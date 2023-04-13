using System.ComponentModel.DataAnnotations;
using System.IdentityModel.Tokens.Jwt;
using System.Security.Claims;
using Exsample.Data;
using Exsample.Models;
using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Mvc;
using Microsoft.IdentityModel.Tokens;

namespace Exsample.Controllers;

[Route("api/[controller]")]
[ApiController]
public class UserController : Controller
{
    public static IWebHostEnvironment _webHostEnvironment;
    
    public UserController(IWebHostEnvironment environment)
    {
        _webHostEnvironment = environment;
    }

    [HttpPost]
    public string AddUser(RegistryUser user)
    {
        Context context = new Context();
        try
        {
            if (user.Login.Length != 0 && user.Password.Length != 0)
            {
                context.User.Add(new User {Login = user.Login,Password = user.Password});
                context.SaveChanges();
                return "Add user";
            }
            else
            {
                return "Not add user";        
            }
        }
        catch (Exception e)
        {
            Console.WriteLine(e);
            throw;
        }
    }
    
    [HttpPost("/authentication")]
    public IActionResult AuthenticationUser(RegistryUser user)
    {
        var identity =  GetIdentity(user.Login, user.Password);
        if (identity == null )
        {
            return  BadRequest(new { errorText = "Invalid username or password." });
        }
 
        var now = DateTime.UtcNow;
        var jwt = new JwtSecurityToken(
            issuer: AuthOptions.ISSUER,
            audience: AuthOptions.AUDIENCE,
            notBefore: now,
            claims: identity.Claims,
            expires: now.Add(TimeSpan.FromMinutes(AuthOptions.LIFETIME)),
            signingCredentials: new SigningCredentials(AuthOptions.GetSymmetricSecurityKey(), SecurityAlgorithms.HmacSha256));
        var encodedJwt = new JwtSecurityTokenHandler().WriteToken(jwt);
 
        var response = new
        {
            access_token = encodedJwt,
            login = identity.Name
        };
        return Json(response);
    }
    
    [HttpPost("/validate")]
    public IActionResult Valid(Token authToken) 
    {
        var handler = new JwtSecurityTokenHandler();
        var ValidateParams =new TokenValidationParameters
        {
            IssuerSigningKey =  new SymmetricSecurityKey(AuthOptions.GetSymmetricSecurityKey().Key),
            ValidateIssuer = false,
            ValidateAudience = false,
            ClockSkew = TimeSpan.Zero
        };
        SecurityToken validateToken = null;
        try
        {
            validateToken = handler.ReadToken(authToken.token);
            handler.ValidateToken(authToken.token, ValidateParams, out validateToken);
        }
        catch(SecurityTokenException)
        {
            return BadRequest(new { errorText = "False" }); 
        }
        return  Ok(Convert.ToString(validateToken !=null));
    }

    private ClaimsIdentity GetIdentity(string login, string password)
    {
        Context context = new Context();
        if (login == null || password == null)
            return null;
        var user = context.User.AsQueryable().Where(t => t.Login == login).ToList()
            .FirstOrDefault(x => x.Login == login && x.Password == password);
        if (user != null)
        {
            var claim = new List<Claim>
            {
                new Claim(ClaimsIdentity.DefaultNameClaimType, user.Login),
                new Claim(ClaimsIdentity.DefaultRoleClaimType, "User")
            };
            ClaimsIdentity claimsIdentity = new ClaimsIdentity(claim,"Token", ClaimsIdentity.DefaultNameClaimType, 
                ClaimsIdentity.DefaultRoleClaimType);
            return claimsIdentity;
        }
        return null;
    }

}