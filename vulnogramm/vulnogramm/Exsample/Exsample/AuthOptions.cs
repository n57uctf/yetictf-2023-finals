using System.Text;
using Microsoft.IdentityModel.Tokens;

namespace Exsample
{
    public class AuthOptions
    {
        public const string ISSUER = "MyAuthServer"; 
        public const string AUDIENCE = "VulnogrammClient"; 
        const string KEY = "VulnogrammVulogramm";
        public const int LIFETIME = 15; 
        public static SymmetricSecurityKey GetSymmetricSecurityKey()
        {
            return new SymmetricSecurityKey(Encoding.ASCII.GetBytes(KEY));
        }
    }
}

