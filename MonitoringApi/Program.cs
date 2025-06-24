using MonitoringApi.Data;
using Microsoft.EntityFrameworkCore;
using Microsoft.Extensions.Configuration;
using System;
using Microsoft.AspNetCore.Builder;
using Microsoft.AspNetCore.Authentication.JwtBearer;
using Microsoft.IdentityModel.Tokens;
using System.Text;

public partial class Program
{
    public static void Main(string[] args)
    {
        var builder = WebApplication.CreateBuilder(args);


        var jwtSettings = builder.Configuration.GetSection("Jwt");
        var key = Encoding.ASCII.GetBytes(jwtSettings["Secret"]);

        builder.Services.AddAuthentication(options =>
        {
            options.DefaultAuthenticateScheme = JwtBearerDefaults.AuthenticationScheme;
            options.DefaultChallengeScheme = JwtBearerDefaults.AuthenticationScheme;
        })
        .AddJwtBearer(options =>
        {
            options.RequireHttpsMetadata = false; 
            options.SaveToken = true;
            options.TokenValidationParameters = new TokenValidationParameters
            {
                ValidateIssuerSigningKey = true,
                IssuerSigningKey = new SymmetricSecurityKey(key),
                ValidateIssuer = true,
                ValidIssuer = jwtSettings["Issuer"],
                ValidateAudience = true,
                ValidAudience = jwtSettings["Audience"],
                ValidateLifetime = true,
                ClockSkew = TimeSpan.Zero 
            };
        });

        builder.Services.AddAuthorization();

        builder.Services.AddControllers().AddJsonOptions(options =>
        {
            options.JsonSerializerOptions.PropertyNameCaseInsensitive = true;
        });


        builder.Services.AddEndpointsApiExplorer();

        builder.Services.AddDbContext<MonitoringContext>(options =>
            options.UseSqlServer(builder.Configuration.GetConnectionString("DefaultConnection")));

        builder.Services.AddHttpClient("LocationIqApiClient", client =>
        {
            var baseUrl = builder.Configuration.GetValue<string>("LocationIq:BaseUrl");
            if (string.IsNullOrEmpty(baseUrl))
            {
                throw new InvalidOperationException("LocationIQ API BaseUrl is not configured in appsettings.json or user secrets.");
            }
            client.BaseAddress = new Uri(baseUrl);
            client.Timeout = TimeSpan.FromSeconds(10);
        });

        builder.Services.AddHttpClient("SensoringApiClient", client =>
        {
            var baseUrl = builder.Configuration.GetValue<string>("SensoringApi:BaseUrl");
            if (string.IsNullOrEmpty(baseUrl))
            {
                throw new InvalidOperationException("Sensoring API BaseUrl is not configured in appsettings.json or user secrets.");
            }
            client.BaseAddress = new Uri(baseUrl);
            client.Timeout = TimeSpan.FromSeconds(30); 
        });

        builder.Services.AddHttpClient("FastApiClient", client =>
        {
            var baseUrl = builder.Configuration.GetValue<string>("FastApiBaseUrl"); 
            if (string.IsNullOrEmpty(baseUrl))
            {
                throw new InvalidOperationException("FastAPI BaseUrl is not configured in appsettings.json or user secrets.");
            }
            client.BaseAddress = new Uri(baseUrl);
            client.Timeout = TimeSpan.FromSeconds(15); 
        });

        builder.Services.AddCors(options =>
        {
            options.AddDefaultPolicy(
                policy =>
                {
                    policy.WithOrigins(
                            "http://127.0.0.1:5500",
                            "http://localhost:5500", 
                            "http://localhost:3000", 
                            "http://127.0.0.1:3000", 
                            "http://127.0.0.1:8000",
                            "https://mrayan007.github.io"
                        )
                        .AllowAnyHeader()
                        .AllowAnyMethod(); 
                });
        });

        var app = builder.Build();

        app.UseHttpsRedirection();

        app.UseCors();

        app.UseAuthentication();
        app.UseAuthorization();

        app.MapControllers();

        using (var scope = app.Services.CreateScope())
        {
            var dbContext = scope.ServiceProvider.GetRequiredService<MonitoringContext>();
            Console.WriteLine("Applying database migrations...");
            try
            {
                dbContext.Database.Migrate();
                Console.WriteLine("Database migrations applied successfully.");
            }
            catch (Exception ex)
            {
                Console.WriteLine($"Error applying database migrations: {ex.Message}");
            }
        }

        app.Run();
    }
}