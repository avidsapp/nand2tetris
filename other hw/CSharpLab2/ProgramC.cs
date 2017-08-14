using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;

namespace IWKS_5300_Lab2
{
  class Person
  {
    public static string City = "Denver";

    // create private internal variables to hold the "real" data and give them a default value
    private string hcr = "Unknown";
    private int years = 0;
    private double wtt = 0.0;
    private double htt = 0.0;

    public string HairColor
    {
      get
      {
        return hcr;
      }
      set
      {
        hcr = value;
      }
    }
    public int Age
    {
      get
      {
        return years;
      }
      set
      {
        // validate age input (people live past 100...)
        if (value <= 100 && value >= 0)
        {
          years = value;
        }
        else
        {
          years = 0;
        }
      }
    }
    public double Height
    {
      get
      {
        return htt;
      }
      set
      {
        htt = value;
      }
    }
    public double Weight
    {
      get
      {
        return wtt;
      }
      set
      {
        wtt = value;
      }
    }

    // Create an explicit constructor for instances of Person
    public Person(string hc, int age, double ht, double wt)
    {
      HairColor = hc;
      Age = age;
      Height = ht;
      Weight = wt;
    }
  }

  class Program
  {
    static void Main(string[] args)
    {
      // Declare and initialize Bob
      Person Bob = new Person("Brown", 21, 72.3, 185.4);
      //Declare and initialize Carol
      Person Carol = new Person("Red", 20, 67.1, 125.7);

      // Make changes to Bob for shits and giggles
      Bob.Age = 55;
      Bob.HairColor = "Blonde";

      // Gonna try to trip up robot validation
      Carol.Age = -140;

      // print some values
      Console.WriteLine("Bob's age = {0}; Bob's height = {1}; Bob's weight = {2}; Bob's hair color = {3}; Bob's city = {4}", Bob.Age, Bob.Height, Bob.Weight, Bob.HairColor, Person.City);

      Console.WriteLine("Carol's age = {0}; Carol's height = {1}; Carol's weight = {2}; Carol's hair color = {3}; Carol's city = {4}", Carol.Age, Carol.Height, Carol.Weight, Carol.HairColor, Person.City);
    }
  }
}
