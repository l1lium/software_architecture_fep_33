#include <iostream>
#include <vector>
#include <string>

using namespace std;

// declaration classes 
class Customer;
class Operator;
class Bill;

class Operator { // Class Operator() - 
public:
    int ID;
private:
    double TalkingCharge;
    double MessageCost;
    double NetworkCharge;
    double DiscountRate;
public:
    Operator() : ID(0), TalkingCharge(0), MessageCost(0), NetworkCharge(0), DiscountRate(0) {}

    Operator(int ID, double TalkingCharge, double MessageCost, double NetworkCharge, double DiscountRate) 
        :ID(ID), TalkingCharge(TalkingCharge), MessageCost(MessageCost), NetworkCharge(NetworkCharge), DiscountRate(DiscountRate) {}

    double getTalking() const {
        return TalkingCharge;
    };
    double setTalking(double charge) {
        TalkingCharge = charge;
    };

    double getMessege() const {
        return MessageCost;
    };
    double setMessege(double cost) {
        MessageCost = cost;
    };

    double getNetwork() const {
        return NetworkCharge;
    };
    double setNetwork(double charge) {
        NetworkCharge = charge;
    };
    
    double getDiscount() const {
        return DiscountRate;
    };
    double setDiscount(double rate) {
        DiscountRate = rate;
    };

    double calculateTalkingCost(int minute, Customer& customer) { // calculating the cost of talk between cuntumer_1 and customer_2
     double TotalCost = minute * TalkingCharge;
     double DiscountedCost = TotalCost - (1 * (DiscountRate / 100));
     return DiscountedCost;
    }
    double calculateMessageCost(int quantity, Customer& customer, Customer& other) { // calculating the cost of messages from cuntumer_1 to customer_2
        double TotalCost = quantity * MessageCost;
        double DiscountedCost = TotalCost - (1 * (DiscountRate / 100));
        return DiscountedCost;
    }
    double calculateNetworkCharge(int amount) { // calculating the cost of used internet trafic 
        double TotalCost = amount * NetworkCharge;
        double DiscountedCost = TotalCost - (1 * (DiscountRate / 100));
        return DiscountedCost;
    }
};

class Bill { // class Bill -

public:
    double limitingAmount;
private:
    double currentDebt;

public:
    Bill(double limit, double Debt) : limitingAmount(limit), currentDebt(Debt) {};

    double getLimit() const {
        return limitingAmount;
    }
    double getDebt() const {
        return currentDebt;
    }

    bool check(double amount) {
        return (currentDebt + amount <= limitingAmount);
    }
    void add(double amount) { // method of adding a new debts to the bill for customer
        if (check(amount)) {
            currentDebt += amount;
        }
        else {
            cout << "Exceeded limit amount. Cannot add debt" << endl;
        }
    }
    void pay(double amount) { // method of paying of the debt for the credit for customer
        if (amount > currentDebt) {
            cout << "Cannot proceed payment, exceedet current debt" << endl;
        }
        else {
            currentDebt -= amount;
        }
    }
    void ChangeTheLimit(double amount) { // methof of changing credit limit for customer
        limitingAmount = amount;
    }

};

class Customer { // class Customer - 

public:
    int ID;
    string FirstName;
    string SecondName;
    int Age;
    Operator* operators;
    Bill* bills;


    Customer(int ID, string FirstName, string SecondName, int Age, Operator* operators, Bill* bills)
        : ID(ID), FirstName(FirstName), SecondName(SecondName), Age(Age) {
        this->operators = operators;
        this->bills = bills;
    }

    int getAge() const {
        return Age;
    }
    void setAge(int age) {
        this->Age = age;
    }

    Operator* getOperators() const {
        return operators;
    }
    void setOperators(Operator* operators) {
        this->operators = operators;
    }

    Bill* getBills() const {
        return bills;
    }
    void setBills(Bill* bills) {
        this->bills = bills;
    }

    void talk(int minute, Customer& other) { 
        cout << "Customer " << FirstName << " " << SecondName << " talked for " << minute << " minutes with " << other.FirstName << " " << other.SecondName << endl;
    }

    void message(int quantity, Customer& other) {
        cout << "Customer " << FirstName << " " << SecondName << " sent " << quantity << " messages to " << other.FirstName << " " << other.SecondName << endl;
    }

    void connection(double amount) {
        cout << "Customer " << FirstName << " " << SecondName << " used " << amount << " MB of internet" << endl;
    }
};
/*
class History : public Customer {
public:
    Customer customer;
    string connectionType;
    float amount;

};
*/

class Main {
public:
   
    static const int MAX_CUSTOMERS = 2;  
    static const int MAX_OPERATORS = 2;  
    static const int MAX_BILLS = 2;

    Customer* customers[MAX_CUSTOMERS]; 
    Operator* operators[MAX_OPERATORS];   
    Bill* bills[MAX_BILLS];
   
/*
    int N, M;
    Customer** customers;
    Operator** operators;
    Bill** bills;
    */

/*
    Main(int numCust, int numOper) {
        N = numCust;
        M = numOper;
        customers = new Customer*[N];
        operators = new Operator*[M];
        bills = new Bill*[N];
    };
*/

    Main() {
        MainData();
    }; 

    void MainData() {

        operators[0] = new Operator(45, 2, 3, 1.5, 0.5);
        operators[1] = new Operator(79, 1.7, 4, 1.2, 0.9);

        bills[0] = new Bill(1000, 3000);
        bills[1] = new Bill(3000, 75000);

        customers[0] = new Customer(12, "Joun", "Fallout", 35, operators[0], bills[0]);
        customers[1] = new Customer(44, "Walter", "White", 48, operators[1], bills[1]);

    }


    /*
    void CreateCustomer() {
    
        for (int i = 0; i < N; ++i) {
        
            cout << "Creating Customer " << i + 1 << ":" << endl;
            string firstName, lastName;
            int age, OperatorIndex;
            double BillLimit, limintingAmount;
            cout << "Enter first name: ";
            cin >> firstName;
            cout << "Enter last name: ";
            cin >> lastName;
            cout << "Enter age: ";
            cin >> age;
            
            cout << "Enter bill limit: ";
            cin >> BillLimit;

            bills[i] = new Bill(BillLimit);

            cout << "Enter Limits";
            cin >> limintingAmount;


            cout << "Choose an operator (0 to " << M - 1 << "): ";
            cin >> OperatorIndex;
            customers[i] = new Customer(i, firstName, lastName, age, operators[OperatorIndex], bills[i], limintingAmount);
        }
    
    };
    */
 //   void CreateOperator();

    void TestTalks() {
        cout << "\n Testing Talk:" << endl;
        customers[0]->talk(5, *customers[1]);
    };
   void testMessage() {
        cout << "\n Testing Message:" << endl;
        customers[1]->message(19, *customers[0]);
    };
   void testConnection() {
       cout << "\n Testing Internet:" << endl;
       customers[0]->connection(89);
   };

   void TestPay() {
       cout << "\n Testing Payment:" << endl;
       cout << "Before payment, customer " << customers[1]->FirstName << "'s debt: " << customers[1]->bills->getDebt() << endl;
       customers[1]->bills->pay(4000);
       cout << "After payment, customer " << customers[1]->FirstName << "'s debt: " << customers[1]->bills->getDebt() << endl;
      
   };
   void TestChangeOper() {
       cout << "\n Testing Changing of Operator:" << endl;
       cout << "Before operator change, customer " << customers[0]->FirstName << " is with Operator ID: " << customers[0]->operators->ID << endl;
       customers[0]->operators = operators[1];
       cout << "After operator change, customer " << customers[0]->FirstName << " is now with Operator ID: " << customers[0]->operators->ID << endl;

   };
   void TestChangeBill() {
       cout << "\n Testing Changing of Bill:" << endl;
       cout << "Before changing bill limit, customer " << customers[1]->FirstName << "'s limit: " << customers[1]->bills->getLimit() << endl;
       customers[1]->bills->ChangeTheLimit(5000);
       cout << "After changing bill limit, customer " << customers[1]->FirstName << "'s limit: " << customers[1]->bills->getLimit() << endl;

   };

   ~Main() {
       // Clean up dynamically allocated memory
       for (int i = 0; i < MAX_CUSTOMERS; ++i) {
           delete customers[i];  
       }
       for (int i = 0; i < MAX_OPERATORS; ++i) {
           delete operators[i]; 
       }
       for (int i = 0; i < MAX_BILLS; ++i) {
           delete bills[i]; 
       }
   }
   

};

int main()
{
  /*
    int N, M;
    cout << "Enter number of Customers (N): ";
    cin >> N;
    cout << "Enter number of Operators (M): ";
    cin >> M;

    Main mainClass(N, M;


   */

    Main mainClass;

    mainClass.TestTalks();
    mainClass.testMessage();
    mainClass.testConnection();
    mainClass.TestPay();
    mainClass.TestChangeOper();
    mainClass.TestChangeBill();



    /*
    Operator operators[2]; 
    Bill bills[3];    

    Customer customer1(1, "Johnº","Doe", 25, operators, bills, 1000.0);
    Customer customer2(2, "Jane", "Smith", 30, operators, bills, 1500.0);

    customer1.talk(10, customer2);      
    customer1.message(5, customer2);    
    customer1.connection(200.0);
 

    Operator operator1(1, 0.5, 0.1, 0.05, 10);

    cout << "Talking cost for 30 minutes: $" << operator1.calculateTalkingCost(30, customer1) << std::endl;
    cout << "Message cost for 50 messages: $" << operator1.calculateMessageCost(50, customer1, customer2) << std::endl;
    cout << "Network cost for 500 MB: $" << operator1.calculateNetworkCharge(500) << std::endl;

    return 0;
    */
}



