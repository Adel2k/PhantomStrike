#include <iostream>
#include <fstream>
#include <sstream>
#include <string>
#include <vector>
#include <json.hpp>  // Include the nlohmann/json library
#include <openssl/ssl.h>
#include <openssl/err.h>
#include <openssl/rand.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <unistd.h>
#include <cstdlib>
#include <platform.h>  // For platform detection

using json = nlohmann::json;

const std::string SERVER_IP = "192.168.56.101"; // Replace with your server's IP address
const int PORT = 1234;
const std::string VIRTUAL_GPUS[] = {"virtual", "vmware", "hyperv"}; // GPU keywords to detect virtual machines

// Helper function to get system's GPU info
std::string get_gpu_info() {
    std::string output;
    std::string os_name = platform::get_system_name();  // Using platform's get_system_name method
    try {
        if (os_name == "linux") {
            output = system("lspci | grep -i vga");
        } else if (os_name == "windows") {
            output = system("wmic path win32_videocontroller get name");
        } else if (os_name == "darwin") {
            output = system("system_profiler SPDisplaysDataType");
        }
    } catch (...) {
        output = "Error";
    }
    return output;
}

// Check if the system is a VM based on GPU info
bool is_vm() {
    std::string gpu_info = get_gpu_info();
    for (const auto& virtual_gpu : VIRTUAL_GPUS) {
        if (gpu_info.find(virtual_gpu) != std::string::npos) {
            return true;
        }
    }
    return false;
}

// Get CVE from line of text
std::string get_cve_from_line(const std::string& line) {
    size_t start = line.find("CVE-");
    if (start != std::string::npos) {
        size_t end = line.find_first_of(" ,", start);
        return line.substr(start, end - start);
    }
    return "";
}

// Perform Nmap scan and collect CVE information
std::vector<json> get_cve(const std::string& target_ip) {
    std::vector<json> cves;
    std::string command = "nmap -p21,25,80 --script vuln " + target_ip + " -oG -";
    std::string result = system(command);

    // Parse the result for CVE entries
    std::istringstream iss(result);
    std::string line;
    while (std::getline(iss, line)) {
        std::string cve = get_cve_from_line(line);
        if (!cve.empty()) {
            cves.push_back({{"port", 80}, {"service", "http"}, {"cve", cve}});
        }
    }

    return cves;
}

// Send the vulnerability report to the server
void send_vuln_report(const std::vector<json>& vuln_data) {
    SSL_CTX* ctx = SSL_CTX_new(TLS_client_method());
    SSL* ssl = SSL_new(ctx);
    BIO* bio = BIO_new_ssl_connect(ctx);
    BIO_set_conn_hostname(bio, SERVER_IP.c_str());
    BIO_set_conn_port(bio, std::to_string(PORT).c_str());

    if (BIO_do_connect(bio) <= 0) {
        std::cerr << "[!] SSL connection failed!" << std::endl;
        return;
    }

    json report_data;
    report_data["vuln_data"] = vuln_data;
    report_data["message"] = is_vm() ? "[!] Error: The system is running in a virtual machine." : "[+] The system is not running in a virtual machine.";
    report_data["is_vm"] = is_vm();

    std::string json_str = report_data.dump();
    BIO_write(bio, json_str.c_str(), json_str.length());

    std::cout << "[+] Sent vulnerability report and VM status." << std::endl;

    BIO_free_all(bio);
    SSL_CTX_free(ctx);
}

int main() {
    std::string target_ip = "192.168.56.101";
    std::vector<json> cve_list = get_cve(target_ip);
    send_vuln_report(cve_list);
    return 0;
}
