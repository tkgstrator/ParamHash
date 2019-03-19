// splam.cpp : このファイルには 'main' 関数が含まれています。プログラム実行の開始と終了がそこで行われます。
//

#include "pch.h"
#include <iostream>
#include <fstream>
#include <sstream>
#include <string>
#include <vector>
#include <Windows.h>

using namespace std;

int main(int argc, char *argv[])
{
	vector<string> param;

	for (int i = 1; i <= argc; i++)
	{
		string path = (string)argv[i];
		int offset = path.find_last_of("\\") + 1;
		string filename = path.substr(0, offset) + "rpl_" + path.substr(offset);

		ofstream ofs(filename);
		ifstream ifs("param.csv");
		string p, line, token;

		while (getline(ifs, line))
		{
			istringstream stream(line);
			while (getline(stream, token, ','))
			{
				param.push_back(token);
			}
		}

		// 変換したいxml読み込み
		ifstream xml(argv[1]);
		while (getline(xml, line))
		{
			int st = line.find("Name=\"") + 6;
			if (st > 6)
			{
				int ed = line.find("\"", st);
				string value = line.substr(st, ed - st);
				auto itr = find(param.begin(), param.end(), value);

				//cout << itr - param.begin() << endl;
				if (itr == param.end())
				{
					p = "unknown";
				}
				else
				{
					p = param[itr - param.begin() + 1];
				}
				line.replace(st, ed - st, p);
			}
			ofs << line << endl;
			;
		}
		ofs.close();
	}
}
