using AMIP.Domain.Interfaces;
using Microsoft.AspNetCore.Mvc;

namespace AMIP.Api.Controllers;

[ApiController]
[Route("api/[controller]")]
public class PredictionsController(IPredictionRepository predictionRepository) : ControllerBase
{
    [HttpGet("latest")]
    public async Task<IActionResult> GetLatest([FromQuery] string symbol)
    {
        var prediction = await predictionRepository.GetLatestPredictionAsync(symbol);
        if (prediction == null) return NotFound();
        return Ok(prediction);
    }

    [HttpGet("history")]
    public async Task<IActionResult> GetHistory([FromQuery] string symbol, [FromQuery] DateTime from, [FromQuery] DateTime to)
    {
        var predictions = await predictionRepository.GetPredictionHistoryAsync(symbol, from, to);
        return Ok(predictions);
    }
}
