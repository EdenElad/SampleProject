import { useState } from "react";
import { SafeAreaView, View, Text, TextInput, Button, ScrollView, Platform } from "react-native";

const DEFAULT_API_BASE =
  Platform.OS === "android"
    ? "http://10.0.2.2:8000" // Android Emulator
    : "http://localhost:8000"; // iOS Simulator

// בטלפון אמיתי: החלף ל-IP של המחשב, לדוגמה:
// const API_BASE = "http://192.168.1.50:8000";
const API_BASE = DEFAULT_API_BASE;

export default function App() {
  const [pingResult, setPingResult] = useState(null);
  const [message, setMessage] = useState("Hello from React Native!");
  const [echoResult, setEchoResult] = useState(null);
  const [error, setError] = useState(null);

  async function doPing() {
    setError(null);
    try {
      const res = await fetch(`${API_BASE}/ping`);
      if (!res.ok) throw new Error(`Ping failed: ${res.status}`);
      setPingResult(await res.json());
    } catch (e) {
      setError(String(e));
    }
  }

  async function doEcho() {
    setError(null);
    try {
      const res = await fetch(`${API_BASE}/echo`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message }),
      });
      if (!res.ok) throw new Error(`Echo failed: ${res.status}`);
      setEchoResult(await res.json());
    } catch (e) {
      setError(String(e));
    }
  }

  return (
    <SafeAreaView style={{ flex: 1, padding: 16 }}>
      <ScrollView>
        <Text style={{ fontSize: 26, fontWeight: "700", marginBottom: 12 }}>
          React Native ↔ FastAPI
        </Text>

        <View style={{ flexDirection: "row", gap: 12, marginBottom: 12 }}>
          <Button title="Ping" onPress={doPing} />
          <Button title="Echo" onPress={doEcho} />
        </View>

        <Text style={{ marginBottom: 6 }}>Message:</Text>
        <TextInput
          value={message}
          onChangeText={setMessage}
          style={{
            borderWidth: 1,
            borderColor: "#999",
            padding: 10,
            borderRadius: 10,
            marginBottom: 12,
          }}
        />

        {error && (
          <Text style={{ color: "red", marginBottom: 12 }}>
            Error: {error}
          </Text>
        )}

        <Text style={{ fontSize: 18, fontWeight: "600" }}>/ping result</Text>
        <Text style={{ fontFamily: "monospace", marginBottom: 12 }}>
          {pingResult ? JSON.stringify(pingResult, null, 2) : "—"}
        </Text>

        <Text style={{ fontSize: 18, fontWeight: "600" }}>/echo result</Text>
        <Text style={{ fontFamily: "monospace" }}>
          {echoResult ? JSON.stringify(echoResult, null, 2) : "—"}
        </Text>
      </ScrollView>
    </SafeAreaView>
  );
}
