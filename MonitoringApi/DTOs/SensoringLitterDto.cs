using System;
using System.Text.Json.Serialization;

namespace MonitoringApi.DTOs
{
    public class SensoringLitterDto
    {
        [JsonPropertyName("id")]
        public Guid Id { get; set; }

        [JsonPropertyName("dateTime")]
        public DateTime DateTime { get; set; }

        [JsonPropertyName("locationLat")] 
        public float LocationLat { get; set; }

        [JsonPropertyName("locationLon")] 
        public float LocationLon { get; set; }

        [JsonPropertyName("category")]
        public string Category { get; set; }

        [JsonPropertyName("confidence")]
        public float Confidence { get; set; }

        [JsonPropertyName("temperature")]
        public float Temperature { get; set; }
    }
}