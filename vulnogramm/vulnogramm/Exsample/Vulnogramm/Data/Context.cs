using Vulnogramm.Models;

namespace Vulnogramm.Data;
using Microsoft.EntityFrameworkCore;

public class Context: DbContext
{
    public Context (DbContextOptions<Context> options) : base(options)
    {
    }
    
    public Context()
    {
        Database.EnsureCreated();
    }
    
    protected override void OnConfiguring(DbContextOptionsBuilder optionsBuilder)
    {
        optionsBuilder.UseNpgsql("Host=db;  Port=5432; Database=Vulnogramm; Username=admin; Password=admin");
    }
    
    protected override void OnModelCreating(ModelBuilder modelBuilder){
        modelBuilder.Entity<User>()
            .Property(p => p.Id).ValueGeneratedOnAdd();
        modelBuilder.Entity<Post>()
            .Property(p => p.Id).ValueGeneratedOnAdd();
    }

    public DbSet<User> User { get; set; }
    public DbSet<Post> Post { get; set; }

}