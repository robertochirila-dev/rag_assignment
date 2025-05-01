import React from "react";
import { render, screen, fireEvent, waitFor } from "@testing-library/react";
import '@testing-library/jest-dom'; 
import ChatInterface from "./ChatInterface";

// Mock fetch globally
beforeEach(() => {
  global.fetch = jest.fn();
});

afterEach(() => {
  jest.resetAllMocks();
});

test("renders input and submit button", () => {
  render(<ChatInterface />);
  expect(screen.getByPlaceholderText(/enter your measurements/i)).toBeInTheDocument();
  expect(screen.getByText(/get recommendation/i)).toBeInTheDocument();
});

test("shows loading spinner on submit", async () => {
  fetch.mockResolvedValueOnce({
    ok: true,
    json: async () => ({
      recommendation: "34D",
      reasoning: "Test reasoning",
      fit_tips: "Test tips",
      identified_issues: [],
      confidence: 1.0,
      sister_sizes: []
    }),
  });

  render(<ChatInterface />);
  fireEvent.change(screen.getByPlaceholderText(/enter your measurements/i), {
    target: { value: "34 underbust, 38 bust" },
  });
  fireEvent.click(screen.getByText(/get recommendation/i));
  expect(screen.getByText(/loading/i)).toBeInTheDocument();
  await waitFor(() => expect(screen.queryByText(/loading/i)).not.toBeInTheDocument());
});

test("displays error message from backend", async () => {
  fetch.mockResolvedValueOnce({
    ok: false,
    json: async () => ({ detail: "Could not extract both underbust and bust measurements." }),
  });

  render(<ChatInterface />);
  fireEvent.change(screen.getByPlaceholderText(/enter your measurements/i), {
    target: { value: "no numbers here" },
  });
  fireEvent.click(screen.getByText(/get recommendation/i));
  await waitFor(() => expect(screen.getByText(/could not extract both underbust/i)).toBeInTheDocument());
});

test("clear button resets messages and input", async () => {
  fetch.mockResolvedValueOnce({
    ok: true,
    json: async () => ({
      recommendation: "34D",
      reasoning: "Test reasoning",
      fit_tips: "Test tips",
      identified_issues: [],
      confidence: 1.0,
      sister_sizes: []
    }),
  });

  render(<ChatInterface />);
  fireEvent.change(screen.getByPlaceholderText(/enter your measurements/i), {
    target: { value: "34 underbust, 38 bust" },
  });
  fireEvent.click(screen.getByText(/get recommendation/i));
  await waitFor(() => screen.getByText(/recommended size/i));
  fireEvent.click(screen.getByText(/clear/i));
  expect(screen.queryByText(/recommended size/i)).not.toBeInTheDocument();
  expect(screen.getByPlaceholderText(/enter your measurements/i)).toHaveValue("");
});
