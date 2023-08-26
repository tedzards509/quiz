import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;

import 'constants.dart';

void main() {
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: Constants.appName,
      theme: ThemeData(
        primarySwatch: Constants.primarySwatch,
        brightness: Brightness.dark,
      ),
      home: const AuthenticationPage(),
    );
  }
}

class AuthenticationPage extends StatelessWidget {
  const AuthenticationPage({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text(Constants.appName),
      ),
      body: const Center(
        child: CodeSender(),
      ),
    );
  }
}

class CodeSender extends StatefulWidget {
  const CodeSender({super.key});

  @override
  State<CodeSender> createState() => _CodeSenderState();
}

class _CodeSenderState extends State<CodeSender> {
  String code = '';
  String name = '';

  Future<void> _onPressed(String code) async {
    final apiEndpoint = Uri.parse('${Constants.apiDomain}/lobby/connect');
    final headers = <String, String>{
      'Content-Type': 'application/json; charset=UTF-8',
    };
    final body = '{"code": "$code", "name": "$name"}';

    try {
      final response =
          await http.post(apiEndpoint, headers: headers, body: body);

      if (response.statusCode == 200) {
        // Successful API call, you can handle the response here
        print('API response: ${response.body}');
      } else {
        // Handle API error here
        print('API Error: ${response.statusCode}, body: ${response.body}');
      }
    } catch (e) {
      // Handle network or other errors here
      print('Error: $e');
    }
  }

  @override
  Widget build(BuildContext context) {
    return Column(
      mainAxisAlignment: MainAxisAlignment.center,
      children: [
        SizedBox(
          width: 100,
          child: TextField(
            decoration: const InputDecoration(
              border: OutlineInputBorder(),
              labelText: 'Name',
            ),
            onChanged: (value) {
              setState(() {
                name = value;
              });
            },
          ),
        ),
        SizedBox(
          width: 100,
          child: TextField(
            decoration: const InputDecoration(
              border: OutlineInputBorder(),
              labelText: 'Code',
            ),
            onChanged: (value) {
              setState(() {
                code = value;
              });
            },
          ),
        ),
        ElevatedButton(
          onPressed: () => _onPressed(code), // FutureBuilder ?
          child: const Text('Submit'),
        ),
      ],
    );
  }
}
