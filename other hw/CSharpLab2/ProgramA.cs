using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;

namespace IWKS_5300_Lab2
{
  class Person
  {
    public static string City = "Denver";
    public string HairColor;
    public int Age;
    public double Height;
    public double Weight;
  }

  class Program
  {
    static void Main(string[] args)
    {
      Person Bob = new Person();
      Person Carol = new Person();

      // Initialize Bob
      Bob.Age = 21;
      Bob.HairColor = "Brown";
      Bob.Weight = 185.4;
      Bob.Height = 72.3;

      // Initialize Carol
      Carol.Age = 20;
      Carol.HairColor = "Red";
      Carol.Weight = 125.7;
      Carol.Height = 67.1;

      // print some values
      Console.WriteLine("Bob's age = {0}; Bob's height = {1}; Bob's weight = {2}; Bob's hair color = {3}; Bob's city = {4}", Bob.Age, Bob.Height, Bob.Weight, Bob.HairColor, Person.City);

      Console.WriteLine("Carol's age = {0}; Carol's height = {1}; Carol's weight = {2}; Carol's hair color = {3}; Carol's city = {4}", Carol.Age, Carol.Height, Carol.Weight, Carol.HairColor, Person.City);
    }
  }
}
