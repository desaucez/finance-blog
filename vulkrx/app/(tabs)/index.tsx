import { NavigationContainer } from '@react-navigation/native';
import { createNativeStackNavigator } from '@react-navigation/native-stack';
import React, { useEffect } from 'react';

// ✅ FIXED IMPORT PATHS — moved up two levels to access `src`
import { initDB } from '../../src/db/database';
import HomeScreen from '../../src/screens/HomeScreen';
import WorkoutScreen from '../../src/screens/WorkoutScreen';

const Stack = createNativeStackNavigator();

export default function App() {
  useEffect(() => {
    initDB(); // Initialize the SQLite DB when the app starts
  }, []);

  return (
    <NavigationContainer>
      <Stack.Navigator initialRouteName="Home">
        <Stack.Screen name="Home" component={HomeScreen} />
        <Stack.Screen name="Workout" component={WorkoutScreen} />
      </Stack.Navigator>
    </NavigationContainer>
  );
}


