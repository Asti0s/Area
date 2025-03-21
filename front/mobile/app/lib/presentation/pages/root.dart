import 'package:flutter/material.dart';
import 'package:go_router/go_router.dart';

import '/config/constants.dart';
import '/data/repositories/auth.dart';
import '/domain/use-cases/auth.dart';

class RootPage extends StatelessWidget {
  const RootPage({super.key});

  @override
  Widget build(BuildContext context) {
    return FutureBuilder<bool>(
      future: IsAuthenticated(AuthRepositoryImpl()).execute(),
      builder: (context, snapshot) {
        if (snapshot.connectionState == ConnectionState.waiting) {
          return const Center(child: CircularProgressIndicator());
        }
        if (snapshot.hasData && snapshot.data == true) {
          WidgetsBinding.instance.addPostFrameCallback((_) {
            context.go(context.namedLocation(RouteEnum.areas.name));
          });
        } else {
          WidgetsBinding.instance.addPostFrameCallback((_) {
            context.go(context.namedLocation(RouteEnum.login.name));
          });
        }
        return const SizedBox();
      },
    );
  }
}
