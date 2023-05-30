using Newtonsoft.Json;
using System;

class Program
{
    static void Main(string[] args)
    {
        string json = @"{
            'items': [
                {
                    'name': 'item1',
                    'value': 10
                },
                {
                    'name': 'item2',
                    'value': 20
                }
            ]
        }";

        dynamic data = JsonConvert.DeserializeObject(json);
        Console.WriteLine(data.items[0].name);
    }
}

Program.Main(new string[0]);