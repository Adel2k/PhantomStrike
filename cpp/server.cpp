#include <iostream>
#include <fstream>
#include <sstream>
#include <string>
#include <vector>
#include <json.hpp>  // Make sure to include the nlohmann/json library
#include <openssl/ssl.h>
#include <openssl/err.h>
#include <openssl/rand.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <unistd.h>

using json = nlohmann::json;

const std::string CERTFILE = "server.crt";
const std::string KEYFILE = "server.key";
const int PORT = 1234;
const std::string REPORT_FILE = "reports.txt";

void save_report(const std::string& ip, const std::string& report) {
    std::ofstream file(REPORT_FILE, std::ios::app);
    file << "[✔] Report from " << ip << "\n";
    file << report << "\n\n";
    std::cout << "[✔] Report saved from " << ip << std::endl;
}

void init_openssl() {
    SSL_load_error_strings();
    OpenSSL_add_ssl_algorithms();
}

void cleanup_openssl() {
    EVP_cleanup();
}

SSL_CTX* create_ssl_context() {
    const SSL_METHOD* method = TLS_server_method();
    SSL_CTX* ctx = SSL_CTX_new(method);
    if (!ctx) {
        std::cerr << "Unable to create SSL context" << std::endl;
        ERR_print_errors_fp(stderr);
        exit(EXIT_FAILURE);
    }

    if (SSL_CTX_use_certificate_file(ctx, CERTFILE.c_str(), SSL_FILETYPE_PEM) <= 0 ||
        SSL_CTX_use_PrivateKey_file(ctx, KEYFILE.c_str(), SSL_FILETYPE_PEM) <= 0) {
        std::cerr << "Unable to load certificate or private key" << std::endl;
        ERR_print_errors_fp(stderr);
        exit(EXIT_FAILURE);
    }
    return ctx;
}

void handle_client(SSL* ssl) {
    char buffer[4096];
    int bytes;

    bytes = SSL_read(ssl, buffer, sizeof(buffer));
    if (bytes <= 0) {
        std::cerr << "Error reading from socket" << std::endl;
        return;
    }

    buffer[bytes] = '\0';
    std::string data(buffer);

    try {
        auto received_data = json::parse(data);

        auto vuln_data = received_data.value("vuln_data", json::array());
        std::string message = received_data.value("message", "No message");
        bool is_vm = received_data.value("is_vm", false);

        std::cout << "[+] Received vulnerability report:" << std::endl;
        for (const auto& vuln : vuln_data) {
            if (vuln.contains("CVE")) {
                std::cout << " - " << vuln["CVE"] << " | " << vuln.value("Severity", "N/A")
                          << " | " << vuln.value("Description", "No description") << std::endl;
            } else {
                std::cout << "[!] Warning: Invalid vulnerability data format." << std::endl;
            }
        }

        std::cout << "[+] Message from client: " << message << std::endl;

        if (is_vm) {
            std::cout << "[!] Target system is a virtual machine!" << std::endl;
        } else {
            std::cout << "[+] Target system is NOT a virtual machine." << std::endl;
        }

        save_report("Client", data);
    } catch (const json::parse_error& e) {
        std::cerr << "[!] Error: Received invalid JSON data" << std::endl;
    }
}

void start_server() {
    init_openssl();

    SSL_CTX* ctx = create_ssl_context();
    int sockfd = socket(AF_INET, SOCK_STREAM, 0);
    if (sockfd < 0) {
        std::cerr << "Unable to create socket" << std::endl;
        exit(EXIT_FAILURE);
    }

    sockaddr_in addr;
    addr.sin_family = AF_INET;
    addr.sin_port = htons(PORT);
    addr.sin_addr.s_addr = INADDR_ANY;

    if (bind(sockfd, (struct sockaddr*)&addr, sizeof(addr)) < 0) {
        std::cerr << "Unable to bind socket" << std::endl;
        exit(EXIT_FAILURE);
    }

    if (listen(sockfd, 1) < 0) {
        std::cerr << "Unable to listen on socket" << std::endl;
        exit(EXIT_FAILURE);
    }

    std::cout << "[*] Secure Server listening on 0.0.0.0:" << PORT << "..." << std::endl;

    while (true) {
        int client_sockfd = accept(sockfd, nullptr, nullptr);
        if (client_sockfd < 0) {
            std::cerr << "Unable to accept connection" << std::endl;
            continue;
        }

        SSL* ssl = SSL_new(ctx);
        SSL_set_fd(ssl, client_sockfd);

        if (SSL_accept(ssl) <= 0) {
            std::cerr << "SSL handshake failed" << std::endl;
            SSL_free(ssl);
            close(client_sockfd);
            continue;
        }

        std::cout << "[+] Connection established!" << std::endl;
        handle_client(ssl);

        SSL_free(ssl);
        close(client_sockfd);
    }

    close(sockfd);
    SSL_CTX_free(ctx);
    cleanup_openssl();
}

int main() {
    start_server();
    return 0;
}
