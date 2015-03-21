/*
* File:   main.cpp
* Author: atamarkin2
*
* Created on June 26, 2014, 5:11 PM
*/

#include <string>
#include "galik_socketstream.h"
#include <cstdlib>
#include <iostream>
#include <stdio.h>
#include <vector>

using namespace std;

using namespace galik;
using namespace galik::net;

std::vector<std::string> &split(const std::string &s, char delim, std::vector<std::string> &elems) {
	size_t start = 0, end = 0;
	while ((end = s.find(delim, start)) != string::npos) {
		elems.push_back(s.substr(start, end - start));
		start = end + 1;
	}
	elems.push_back(s.substr(start));
	return elems;
}

/*
*
*/
int main(int argc, char** argv) {
	if (argc < 5) {
		cout << "args: <user> <password> <host> <port> <command>" << endl;
		cout << argc;
		exit(1);
	}

	string name(argv[1]);
	string password(argv[2]);

	socketstream ss;
	ss.open(argv[3], atoi(argv[4]));

	string command("");
	for (int i = 5; i < argc; i++) {
		command += argv[i];
		command += " ";
	}
	command;

	ss << name << " " << password << "\n" << command << "\nCLOSE_CONNECTION" << endl;

	while (ss.good() && !ss.eof()) {
		string line;
		getline(ss, line);
		cout << line << endl;
	}
	return 0;
}
