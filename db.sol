//SPDX-License-Identifier: MIT
pragma solidity ^0.8.7;

contract Session {
    string public username;
    uint256 public login_datetime = 0;
    uint256 public logout_datetime = 0;

    constructor(string memory _username, uint256 login) {
        username = _username;
        login_datetime = login;
    }

    function logoutSession(uint256 logout) public {
        logout_datetime = logout;
    }
}

contract Appointment {
    string username;
    uint256 appointment_datetime;
    bool completed = false;
    string prescription = "None";

    constructor(string memory _username, uint256 _appointment_datetime) {
        username = _username;
        appointment_datetime = _appointment_datetime;
    }

    function changeAppointmentDate(uint256 new_appointment_datetime) public {
        appointment_datetime = new_appointment_datetime;
    }

    function changePrescription(string memory _prescription) public {
        prescription = _prescription;
    }

    function completeAppointment() public {
        completed = true;
    }
}

contract Users {
    event loginEvent(address value);
    event userAppointments(address[] appt);

    struct UserData {
        string username;
        bytes32 password;
        string sex;
        uint256 height;
        uint256 weight;
        string role;
        bool new_person;
    }

    mapping(string => UserData) private users;
    string[] users_lookup;

    mapping(string => address) private sessions;
    address[] sessions_lookup;

    mapping(address => string) private appointments;
    address[] appointments_lookup;

    function createUser(string memory _username, string memory _password)
        public
    {
        require(
            compareStrings(users[_username].username, ""),
            "Username already taken"
        );
        bytes32 hashed_password;
        hashed_password = keccak256(abi.encodePacked(_password));
        UserData memory newUser = UserData(
            _username,
            hashed_password,
            "",
            0,
            0,
            "user",
            true
        );
        users[_username] = newUser;
        users_lookup.push(_username);
    }

    function createAppointment(
        string memory _username,
        uint256 _appointment_datetime
    ) public {
        Appointment appointment = new Appointment(
            _username,
            _appointment_datetime
        );
        appointments[address(appointment)] = _username;
        appointments_lookup.push(address(appointment));
    }

    function login(string memory _username, string memory _password) public {
        bytes32 hashed_password;
        hashed_password = keccak256(abi.encodePacked(_password));
        require(
            comparePassword(hashed_password, users[_username].password),
            "Incorrect password"
        );

        Session session = new Session(_username, block.timestamp);
        sessions[_username] = address(session);
        sessions_lookup.push(address(session));
        emit loginEvent(address(session));
    }

    function logout(address session) public {
        Session(session).logoutSession(block.timestamp);
    }

    function giveRole(string memory _username, string memory _role) public {
        for (uint256 i = 0; i < users_lookup.length; i++) {
            if (compareStrings(users_lookup[i], _username)) {
                users[users_lookup[i]].role = _role;
            }
        }
    }

    function updateNewcomer(
        string memory _username,
        string memory _sex,
        uint256 _height,
        uint256 _weight
    ) public {
        users[_username].sex = _sex;
        users[_username].height = _height;
        users[_username].weight = _weight;
        users[_username].new_person = false;
        users[_username].new_person = false;
    }

    function getUser(string memory _username)
        external
        view
        returns (
            string memory username,
            bytes32 password,
            string memory sex,
            uint256 height,
            uint256 weight,
            string memory role,
            bool new_person
        )
    {
        return (
            users[_username].username,
            users[_username].password,
            users[_username].sex,
            users[_username].height,
            users[_username].weight,
            users[_username].role,
            users[_username].new_person
        );
    }

    function getUserAppointments(string memory _username)
        public
        returns (address[] memory)
    {
        uint256 appointment_count = 0;
        for (uint256 i = 0; i < appointments_lookup.length; i++) {
            if (
                compareStrings(_username, appointments[appointments_lookup[i]])
            ) {
                appointment_count++;
            }
        }

        uint256 j = 0;
        address[] memory user_appointments = new address[](appointment_count);
        for (uint256 i = 0; i < appointments_lookup.length; i++) {
            if (
                compareStrings(_username, appointments[appointments_lookup[i]])
            ) {
                user_appointments[j] = appointments_lookup[i];
                j++;
            }
        }
        emit userAppointments(user_appointments);
        return user_appointments;
    }

    function getAllUsers() public view returns (UserData[] memory) {
        UserData[] memory allUsers = new UserData[](users_lookup.length);
        for (uint256 i = 0; i < users_lookup.length; i++) {
            allUsers[i] = users[users_lookup[i]];
        }
        return allUsers;
    }

    function getAllAppointments() public view returns (address[] memory) {
        return appointments_lookup;
    }

    function comparePassword(bytes32 a, bytes32 b) public pure returns (bool) {
        return a == b;
    }

    function compareStrings(string memory a, string memory b)
        public
        pure
        returns (bool)
    {
        return (keccak256(abi.encodePacked(a)) ==
            keccak256(abi.encodePacked(b)));
    }
}
