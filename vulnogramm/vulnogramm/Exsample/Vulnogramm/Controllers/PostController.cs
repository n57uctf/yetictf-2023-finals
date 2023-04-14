using Microsoft.AspNetCore.Mvc;
using System.IO;
using System;
using Vulnogramm.Data;
using Vulnogramm.ImageMethods;
using Vulnogramm.Models;

namespace Vulnogramm.Controllers;


[ApiController]
public class PostController : Controller 
{
    public static IWebHostEnvironment _webHostEnvironment;

    public PostController(IWebHostEnvironment environment)
    {
        _webHostEnvironment = environment;
    }

    [HttpPost("backend/post")]
    public IActionResult Post(NewPost newPost)
    {
        Context context = new Context();
        newPost.photo = newPost.photo.Substring(newPost.photo.IndexOf(',')+1);
        try
        {
            if (newPost.photo.Length > 0 )
            {
                
                if (!Directory.Exists(_webHostEnvironment.WebRootPath+"uploads/"))
                {
                    Directory.CreateDirectory(_webHostEnvironment.WebRootPath+"uploads");
                }
                string path = _webHostEnvironment.WebRootPath + "uploads/" + Path.GetRandomFileName() + ".png";
                if (newPost.method == 0)
                {
                    System.IO.File.WriteAllBytes(path,Convert.FromBase64String(newPost.photo));
                    Magick magick = new Magick(path);
                    magick.TheLastofUS(newPost.sign);
                    newPost.photo = path;
                }
                if (newPost.method == 1)
                {
                    System.IO.File.WriteAllBytes(path,Convert.FromBase64String(newPost.photo));
                    Magick magick = new Magick(path);
                    magick.Fibi(newPost.sign);
                    newPost.photo = path;
                }
                if (newPost.method == 2)
                {
                    System.IO.File.WriteAllBytes(path,Convert.FromBase64String(newPost.photo));
                    Magick magick = new Magick(path);
                    magick.NewText(newPost.sign);
                    newPost.photo = path;
                }
                context.Post.Add(new Post
                {
                    Owner = newPost.Owner,
                    Subscript = newPost.subscript,
                    PhotoForAll = newPost.photo,
                });
                context.SaveChanges();
                var post= context.Post.AsQueryable().Where(t => t.Owner == newPost.Owner).ToList().LastOrDefault();
                Int64 id = post.Id;
                return Json(id);   
            }
            else
            {
                return BadRequest(new { errorText = "Not added"});
            }
        }
        catch (Exception e)
        {
            Console.WriteLine(e);
            throw;
        }
    }
    [HttpPost("backend/feed")]
    public IActionResult AddFeed()
    {
        Context context = new Context();
        var posts = context.Post.AsQueryable().ToList();
        foreach (var post in posts )
        {
            string path = post.PhotoForAll ;
            Magick magick = new Magick(path);
            string newPath = magick.Watermark();
            while (!System.IO.File.Exists(newPath))
            {
                Thread.Sleep(100);
            }
            var file = System.IO.File.ReadAllBytes(newPath);
            var base64File = Convert.ToBase64String(file);
            post.PhotoForAll= base64File;
            base64File = null;
            System.IO.File.Delete(newPath);
        }
        return  Json(posts);
    }
    [HttpPost("backend/yourpost")]
    public IActionResult ShowPost(ShowPost showpost)
    {
        Context context = new Context();
        var post = context.Post.AsQueryable().Where(t => t.Id == showpost.id).ToList()  
            .FirstOrDefault(t => t.Id == showpost.id 
            && t.Owner == showpost.owner);
        if (post != null)
            post.PhotoForAll = Convert.ToBase64String(System.IO.File.ReadAllBytes(post.PhotoForAll));
        return Json(post);
    }
}