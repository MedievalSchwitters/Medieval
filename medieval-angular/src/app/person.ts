export class Person {
    name: string;
    alive = true;
    children: Person[] = [];
    age: number;
    fertile:boolean;

    constructor(name: string){
        this.name = name;
        this.age = 0;
        this.fertile = false; 
    }
}