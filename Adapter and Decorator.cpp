
#include <iostream>
#include <string>
#include <unordered_map>
#include <openssl/sha.h>
#include <sstream>
#include <iomanip>
#include <vector>
#include <memory>

using namespace std;

#pragma warning(disable : 4996)

class CreditCard {
public:
    string client;
    string account_number;
    float credit_limit;
    int grace_period;

  
    CreditCard(string cl, string acc, float limit, int period)
        : client(cl), account_number(acc), credit_limit(limit), grace_period(period) {}

    unordered_map<string, string> give_bank_details() {
        return {
            {"client", client},
            {"account_number", account_number},
            {"credit_limit", to_string(credit_limit)},
            {"grace_period", to_string(grace_period)}
        };
    }

    // Property for setting and getting hashed cvv
    void set_cvv(int cvv_val) { encrypt(to_string(cvv_val)); }
    bool validate_cvv(int input_cvv) { return decrypt(to_string(input_cvv)); }

private:
    string cvv;
    string hashedCvv;

    // Helper function to convert bytes to a hexadecimal string
    string bytesToHex(const unsigned char* bytes, size_t length) {
        stringstream ss;
        for (size_t i = 0; i < length; ++i) {
            ss << hex << setw(2) << setfill('0') << (int)bytes[i];
        }
        return ss.str();
    }

    void encrypt(const string& cvvInput) {
        cvv = cvvInput;

        unsigned char hash[SHA256_DIGEST_LENGTH];
        SHA256_CTX sha256Context;
        SHA256_Init(&sha256Context);
        SHA256_Update(&sha256Context, cvv.c_str(), cvv.size());
        SHA256_Final(hash, &sha256Context);

        hashedCvv = bytesToHex(hash, SHA256_DIGEST_LENGTH);
    }

    bool decrypt(const string& inputCvv) {
        unsigned char hash[SHA256_DIGEST_LENGTH];
        SHA256_CTX sha256Context;
        SHA256_Init(&sha256Context);
        SHA256_Update(&sha256Context, inputCvv.c_str(), inputCvv.size());
        SHA256_Final(hash, &sha256Context);

        string hashedInputCvv = bytesToHex(hash, SHA256_DIGEST_LENGTH);

        // Compare the hashed input CVV with the stored hashed CVV
        return hashedInputCvv == hashedCvv;
    }
};


class BankInfo {
public:
    string bank_name;
    string holder_name;
    vector<string> accounts_number;
    unordered_map<string, vector<string>> credit_history;

    // Retrieve transactions for a specific account
    vector<string> transaction_list(const string& account_number) {
        return credit_history[account_number];
    }
};


class PersonalInfo {
public:
    string name;
    string address;
};

class BankCustomer {
public:
    shared_ptr<CreditCard> credit_card;
    PersonalInfo personal_info;

    BankCustomer(PersonalInfo info, shared_ptr<CreditCard> card)
        : personal_info(info), credit_card(card) {}

    unordered_map<string, string> give_bank_details() {
        unordered_map<string, string> details = credit_card->give_bank_details();
        details["name"] = personal_info.name;
        return details;
    }
};



class GoldenCreditCard : public CreditCard {
public:
    GoldenCreditCard(string cl, string acc, float limit, int period)
        : CreditCard(cl, acc, limit, period) {}

    void exclusive_rewards() {
        cout << "Golden card rewards activated." << endl;
    }
};

class CorporateCreditCard : public CreditCard {
public:
    CorporateCreditCard(string cl, string acc, float limit, int period)
        : CreditCard(cl, acc, limit, period) {}

    void business_insurance() {
        cout << "Corporate card insurance activated." << endl;
    }
};

class VIPCustomer : public BankCustomer {
public:
    VIPCustomer(PersonalInfo info, shared_ptr<CreditCard> card)
        : BankCustomer(info, card) {}

    void access_vip_services() {
        cout << "Accessing VIP customer services." << endl;
    }
};



int main() {
    PersonalInfo p_info = { "John Doe", "123 Elm Street" };
    auto card = make_shared<GoldenCreditCard>("John Doe", "12345678", 5000.0f, 30);
    card->set_cvv(123);

    BankCustomer customer(p_info, card);
    auto details = customer.give_bank_details();

    cout << "Bank Details:" << endl;
    for (const auto& pair : details) {
        cout << pair.first << ": " << pair.second << endl;
    }

    // Decorator usage
    card->exclusive_rewards();
    VIPCustomer vip_customer(p_info, card);
    vip_customer.access_vip_services();

    return 0;
}































































/*

#include <iostream>
#include <string>
#include <openssl/sha.h>
#include <iomanip>
#include <sstream>

#pragma warning(disable : 4996)

using namespace std;

class CreditCard {
private:
    string cvv;
    string hashedCvv;  // Store the hashed version of the CVV

    // Helper function to convert bytes to hexadecimal string
    string bytesToHex(const unsigned char* bytes, size_t length) {
        stringstream ss;
        for (size_t i = 0; i < length; ++i) {
            ss << hex << setw(2) << setfill('0') << (int)bytes[i];
        }
        return ss.str();
    }

public:
    // Encrypt (Hash) the CVV
    void encrypt(const string& cvvInput) {
        cvv = cvvInput;

        // Use SHA256 for hashing the CVV (You can use AES for real encryption)
        unsigned char hash[SHA256_DIGEST_LENGTH];
        SHA256_CTX sha256Context;
        SHA256_Init(&sha256Context);
        SHA256_Update(&sha256Context, cvv.c_str(), cvv.size());
        SHA256_Final(hash, &sha256Context);

        // Store the hashed CVV
        hashedCvv = bytesToHex(hash, SHA256_DIGEST_LENGTH);
    }

    // Decrypt (Verify) the CVV
    bool decrypt(const string& inputCvv) {
        string hashedInputCvv;
        unsigned char hash[SHA256_DIGEST_LENGTH];
        SHA256_CTX sha256Context;
        SHA256_Init(&sha256Context);
        SHA256_Update(&sha256Context, inputCvv.c_str(), inputCvv.size());
        SHA256_Final(hash, &sha256Context);

        hashedInputCvv = bytesToHex(hash, SHA256_DIGEST_LENGTH);

        // Compare the hashed CVV
        return hashedInputCvv == hashedCvv;
    }

    // Getter for the hashed CVV (for debugging purposes)
    string getHashedCvv() const {
        return hashedCvv;
    }
};

int main() {
    CreditCard card;
    string cvv = "123"; // Example CVV input

    // Encrypt the CVV
    card.encrypt(cvv);
    cout << "Hashed CVV: " << card.getHashedCvv() << endl;

    // Verify CVV using the decrypt method
    if (card.decrypt("123")) {
        cout << "CVV is correct!" << endl;
    }
    else {
        cout << "Invalid CVV!" << endl;
    }

    return 0;
}

*/