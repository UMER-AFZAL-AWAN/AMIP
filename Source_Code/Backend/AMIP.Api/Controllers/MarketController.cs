using AMIP.Domain.Interfaces;
using Microsoft.AspNetCore.Mvc;

namespace AMIP.Api.Controllers;

[ApiController]
[Route("api/[controller]")]
public class MarketController(IMarketDataIngestionService ingestionService, IMarketDataRepository marketDataRepository) : ControllerBase
{
    [HttpPost("ingest")]
    public async Task<IActionResult> Ingest([FromQuery] string symbol, [FromQuery] string interval)
    {
        await ingestionService.IngestHistoricalDataAsync(symbol, interval);
        return Ok(new { Message = "Ingestion started" });
    }

    [HttpGet("latest")]
    public async Task<IActionResult> GetLatest([FromQuery] string exchange, [FromQuery] string symbol, [FromQuery] string interval)
    {
        if (!Enum.TryParse(exchange, true, out AMIP.Domain.Enums.ExchangeType exchangeEnum)) return BadRequest("Invalid exchange");
        if (!Enum.TryParse(interval, true, out AMIP.Domain.Enums.CandleInterval intervalEnum)) return BadRequest("Invalid interval");

        var candle = await marketDataRepository.GetLatestCandleAsync(exchangeEnum, symbol, intervalEnum);
        if (candle == null) return NotFound();

        return Ok(candle);
    }

    [HttpGet("candles")]
    public async Task<IActionResult> GetCandles([FromQuery] string exchange, [FromQuery] string symbol, [FromQuery] string interval, [FromQuery] DateTime from, [FromQuery] DateTime to)
    {
        if (!Enum.TryParse(exchange, true, out AMIP.Domain.Enums.ExchangeType exchangeEnum)) return BadRequest("Invalid exchange");
        if (!Enum.TryParse(interval, true, out AMIP.Domain.Enums.CandleInterval intervalEnum)) return BadRequest("Invalid interval");

        var candles = await marketDataRepository.GetCandlesAsync(exchangeEnum, symbol, intervalEnum, from, to);
        return Ok(candles);
    }
}
