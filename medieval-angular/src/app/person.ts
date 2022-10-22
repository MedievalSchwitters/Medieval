export class Person {
    key: number
    name: string;
    alive = true;
    children: Person[] = [];
    age: number;
    fertile:boolean;

    constructor(key: number, name: string){
        this.key = key;
        this.name = name;
        this.age = 0;
        this.fertile = false; 
    }
}