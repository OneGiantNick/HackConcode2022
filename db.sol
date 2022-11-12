// SPDX-Licence-Identifier: MIT
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

    constructor(string memory _username, uint256 _appointment_datetime) {
        username = _username;
        appointment_datetime = _appointment_datetime;
    }
}

contract Users {
    event loginEvent(address value);
    event logoutEvent(string value);

    struct UserData {
        string username;
        bytes32 password;
    }

    mapping(string => UserData) private users;
    string[] users_lookup;

    mapping(string => address) private sessions;
    address[] sessions_lookup;

    mapping(address => string) private appointments;
    address[] addresses_lookup;

    function createUser(string memory _username, string memory _password)
        public
    {
        require(
            compareStrings(users[_username].username, ""),
            "Username already taken"
        );
        bytes32 hashed_password;
        hashed_password = keccak256(abi.encodePacked(_password));
        UserData memory newUser = UserData(_username, hashed_password);
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
        addresses_lookup.push(address(appointment));
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

    function getUser(string memory _username)
        external
        view
        returns (UserData memory)
    {
        return users[_username];
    }

    function getAllUsers() public view returns (UserData[] memory) {
        UserData[] memory allUsers = new UserData[](users_lookup.length);
        for (uint256 i = 0; i < users_lookup.length; i++) {
            allUsers[i] = users[users_lookup[i]];
        }
        return allUsers;
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
