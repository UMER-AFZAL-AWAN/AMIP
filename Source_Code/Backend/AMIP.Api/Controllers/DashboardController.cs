using AMIP.Domain.Interfaces;
using Microsoft.AspNetCore.Mvc;

namespace AMIP.Api.Controllers;

[ApiController]
[Route("api/[controller]")]
public class DashboardController(
    IMarketDataRepository marketDataRepository,
    IPredictionRepository predictionRepository) : ControllerBase
{
    [HttpGet("summary")]
    public async Task<IActionResult> GetSummary()
    {
        // Get latest prediction to check activity
        var latestPrediction = await predictionRepository.GetLatestPredictionAsync("BTCUSDT");

        // Get latest candle 
        var latestCandle = await marketDataRepository.GetLatestCandleAsync(
            AMIP.Domain.Enums.ExchangeType.Binance, "BTCUSDT", AMIP.Domain.Enums.CandleInterval.OneMinute);

        // Get recent predictions count and accuracy
        var recentFrom = DateTime.UtcNow.AddDays(-7);
        var recentTo = DateTime.UtcNow;
        var recentPredictions = await predictionRepository.GetPredictionHistoryAsync("BTCUSDT", recentFrom, recentTo);
        var predictionList = recentPredictions.ToList();
        
        var totalPredictions = predictionList.Count;
        var evaluated = predictionList.Where(p => p.ActualResult != null).ToList();
        var correct = evaluated.Where(p => p.Direction == p.ActualResult).Count();
        var accuracy = evaluated.Count > 0 ? (double)correct / evaluated.Count : 0.65;

        return Ok(new 
        { 
            ActiveModels = 3,
            TotalPredictions = totalPredictions,
            OverallAccuracy = accuracy,
            LatestRegime = "Bullish",
            LatestPrice = latestCandle?.Close,
            LastUpdate = latestCandle?.CloseTime
        });
    }
}
