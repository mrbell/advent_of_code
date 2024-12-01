use std::fs;
use std::str;


fn main() {

    let file_path: String = "./inputs/day01.txt".to_string();
    
    println!("In file {file_path}");

    let contents = fs::read_to_string(file_path)
        .expect("Should have been able to read the file");

    let lines = contents.lines();

    let mut list1: Vec<i32> = Vec::new();
    let mut list2: Vec<i32> = Vec::new();

    for line in lines {
        let line_parts: Vec<&str> = line.split("   ").collect();
        let num1: i32 = line_parts[0].parse().unwrap();
        let num2: i32 = line_parts[1].parse().unwrap();
        list1.push(num1);
        list2.push(num2);        
    }

    list1.sort();
    list2.sort();

    let mut sum1: i32 = 0;

    for i in 0..list1.len() {
        sum1 = sum1 + (list1[i] - list2[i]).abs();
    }

    println!("Part 1: {}", sum1);

    let mut sum2: i32 = 0;

    for i in 0..list1.len() {
        let num = list1[i];
        let mut num_count: i32 = 0;
        for j in 0..list2.len() {
            if list2[j] == num {
                num_count = num_count + 1;
            }
        }
        sum2 = sum2 + num_count * num;
    }

    println!("Part 2: {}", sum2);

}
