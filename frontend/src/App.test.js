import { render, screen } from "@testing-library/react";
import App from "./App";

test("loads dashboard data from the public stats file", async () => {
  global.fetch = jest.fn().mockResolvedValue({
    ok: true,
    json: async () => ({
      metadata: {
        username: "modisee",
        total_games: 2,
        wins: 1,
        losses: 1,
        draws: 0,
        win_rate_percentage: 50,
      },
      ratings: { blitz_avg: 100, rapid_avg: 200, bullet_avg: 300 },
      openings: [],
      history: [],
    }),
  });

  render(<App />);

  expect(global.fetch).toHaveBeenCalledWith("/stats.json");
  expect(
    await screen.findByText(/Chess.com Executive Dashboard/i),
  ).toBeInTheDocument();
});
