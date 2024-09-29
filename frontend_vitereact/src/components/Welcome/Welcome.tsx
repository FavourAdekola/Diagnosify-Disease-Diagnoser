import { Anchor, Text, Title } from '@mantine/core';
import classes from './Welcome.module.css';

export function Welcome() {
  return (
    <>
      <Title className={classes.title} ta="center" mt={100}>
        Welcome to{' '}
        <Text inherit variant="gradient" component="span" gradient={{ from: 'pink', to: 'yellow' }}>
          Dianogisfy
        </Text>
      </Title>
      <Text c="dimmed" ta="center" size="lg" maw={580} mx="auto" mt="xl">
        Diagnosify is a cutting-edge tool that uses artificial intelligence to analyze your symptoms and provide potential diagnoses. Simply describe your medical symptoms in detail, and let our AI model, trained on extensive medical data, suggest possible conditions.
      </Text>
      <Text c="dimmed" ta="center" size="lg" maw={580} mx="auto" mt="xl">
        A HackGT11 Project.
      </Text>
    </>
  );
}
