import { ColorSchemeToggle } from '../components/ColorSchemeToggle/ColorSchemeToggle';
import { Welcome } from '../components/Welcome/Welcome';
import { MultiSelect } from '@mantine/core';
import { Text, Button, Group, Textarea, Paper, Loader } from '@mantine/core';
import { useState } from 'react';

export function HomePage() {
  const [loading, setLoading] = useState(false);
  const [response, setResponse] = useState('');
  const [inputText, setInputText] = useState(''); // Added state for input text

  const handleSubmit = async () => {
    setLoading(true); // Set loading to true when starting request

    try {
      const res = await fetch('http://localhost:5000/predict', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ input_text: inputText }), // Send input text to backend
      });

      if (!res.ok) {
        throw new Error('Network response was not ok');
      }

      const data = await res.json();
      setResponse(data.output_text); // Store response from the server
    } catch (error) {
      console.error('Error:', error);
      setResponse('Error occurred while fetching data'); // Set error message
    } finally {
      setLoading(false); // Set loading to false after request
    }
  };
return (
    <>
      <Welcome />

      <Group justify="center" mt="xl">
        <Textarea
          label="Describe the symptoms you're experiencing in full detail."
          autosize
          minRows={4}
          style={{ width: '50%' }}
          value={inputText} // Bind the Textarea value to inputText state
          onChange={(e) => setInputText(e.currentTarget.value)} // Capture the input text
        />
      </Group>

      <Group justify="center" mt="xl">
        <Button variant="gradient" gradient={{ from: 'pink', to: 'yellow' }} onClick={handleSubmit}>
          Submit
        </Button>
      </Group>

      {loading && (
        <Group justify="center" mt="xl">
          <Loader />
        </Group>
      )}

      <Group justify="center" mt="101">
        <Paper shadow="xl" radius="lg" withBorder p="xl">
          <Text ta="center">{response || 'Awaiting response...'}</Text>
        </Paper>
      </Group>
    </>
  );
}