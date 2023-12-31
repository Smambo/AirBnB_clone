#!/usr/bin/python3
"""command interpreter"""
import cmd
import shlex
from shlex import split
from models.base_model import BaseModel
from models.user import User
from models.place import Place
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.review import Review
from models import storage


class HBNBCommand(cmd.Cmd, BaseModel):
    """
    class to define all command interpreter behaviour
    """
    prompt = "(hbnb) "
    __classes = {
            "BaseModel": BaseModel,
            "User": User,
            "Place": Place,
            "State": State,
            "City": City,
            "Amenity": Amenity,
            "Review": Review,
            }

    def emptyline(self):
        """handles empty lines"""
        pass

    def postcmd(self, stop, line):
        """handles end of file(Ctrl^D) command"""
        return cmd.Cmd.postcmd(self, stop, line)

    def do_quit(self, line):
        """handles (quit) command"""
        return True

    def help_quit(self):
        """(quit) command documentation"""
        print("Quit command to exit the program")

    def do_EOF(self, line):
        """handles end of file command"""
        return True

    def help_EOF(self):
        """(EOF) command documentation"""
        print("EOF command to exit the program")

    def do_create(self, line):
        """
        handles (create) command
        On success, a instance is created, and
        a the id is printed
        """
        if not line:
            print("** class name missing **")
            return
        args = line.split()
        if line:
            if args[0] not in HBNBCommand.__classes:
                print("** class doesn't exist **")
                return
            if args[0] in HBNBCommand.__classes:
                class_name = args[0]
                instance = self.__classes[class_name]()
                instance.save()
                print(instance.id)

    def help_create(self):
        """(create) command documentation"""
        print("creates an instance")

    def do_show(self, line):
        """prints the string representation of a class instance"""
        if not line:
            print("** class name missing **")
            return
        args = line.split()
        if args[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
            return
        if len(args) == 1:
            print("** instance id missing **")
            return
        key = args[0] + "." + args[1]
        if key not in storage.all().keys():
            print("** no instance found **")
            return
        else:
            print(storage.all()[key])

    def help_show(self):
        """(show) command documentation"""
        print("prints the string representation of a class instance")

    def do_destroy(self, line):
        """deletes an instance"""
        if not line:
            print("** class name missing **")
            return
        args = line.split()
        if args[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
            return
        if len(args) == 1:
            print("** instance id missing **")
            return
        key = args[0] + "." + args[1]
        if key not in storage.all().keys():
            print("** no instance found **")
            return
        else:
            class_name = args[0]
            instance = self.__classes[class_name]
            instance_id = args[1]
            del storage.all()["{}.{}".format(args[0], args[1])]
            storage.save()

    def help_destroy(self):
        """(destroy) command documentation"""
        print("deletes an instance")

    def do_all(self, line):
        """prints all string representation of all instances"""
        objectList = []
        args = line.split()
        if not line:
            for obj in storage.all().values():
                objectList.append(str(obj))
            print(objectList)

        elif args[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
            return
        else:
            class_name = args[0]
            for obj in storage.all().values():
                if obj.__class__.__name__ == class_name:
                    objectList.append(str(obj))
            print(objectList)

    def help_all(self):
        """(all) command documentation"""
        print("prints all string representation of all instances")

    def do_update(self, line):
        """updates an instance"""
        if not line:
            print("** class name missing **")
            return
        args = line.split()
        class_name = args[0]
        if class_name not in HBNBCommand.__classes:
            print("** class doesn't exist **")
            return
        if len(args) == 1:
            print("** instance id missing **")
            return
        key = class_name + "." + args[1]
        if key not in storage.all().keys():
            print("** no instance found **")
            return
        if len(args) == 2:
            print("** attribute name missing **")
            return
        if len(args) == 3:
            print("** value missing **")
            return
        key = "{}.{}".format(class_name, args[1])
        obj = storage.all()[key]
        setattr(obj, args[2], args[3])
        obj.save()

    def help_update(self):
        """(update) command documentation"""
        print("updates an instance")

    def stripper(self, s):
        """Strips line"""
        new_str = s[s.find("(")+1:s.rfind(")")]
        new_str = shlex.shlex(new_str, posix=True)
        new_str.whitespace += ','
        new_str.whitespace_split = True
        return list(new_str)

    def dict_stripper(self, s):
        """
        Finds a dict while stripping line.
        """
        new_str = s[s.find("(")+1:s.rfind(")")]
        try:
            new_dict = new_str[new_str.find("{")+1:new_str.rfind("}")]
            return eval("{" + new_dict + "}")
        except Exception:
            return None

    def default(self, line):
        """Default commands."""
        sub_arg = self.stripper(line)
        args = list(shlex.shlex(line, posix=True))
        if args[0] not in HBNBCommand.__classes:
            print("** Unknown syntax: {}".format(line))
            return
        if args[2] == "all":
            self.do_all(args[0])
        elif args[2] == "count":
            count = 0
            for obj in storage.all().values():
                if args[0] == type(obj).__name__:
                    count += 1
            print(count)
            return
        elif args[2] == "show":
            key = args[0] + " " + sub_arg[0]
            self.do_show(key)
        elif args[2] == "destroy":
            key = args[0] + " " + sub_arg[0]
            self.do_destroy(key)
        elif args[2] == "update":
            """
            id_key = args[0] + "." + sub_arg[0]
            new_dict = sub_arg[1] + " " + sub_arg[2]
            self.do_update(id_key)
            """
            new_dict = self.dict_stripper(line)
            if type(new_dict) is dict:
                for key, val in new_dict.items():
                    key_value = args[0] + " " + sub_arg[0]
                    self.do_update(key_value + " " + '{} {}'.format(key, val))
            else:
                key = args[0]
                for arg in sub_arg:
                    key = key + " " + '{}'.format(arg)
                self.do_update(key)
        else:
            print("** Unknown syntax: {}".format(line))
            return


if __name__ == '__main__':
    HBNBCommand().cmdloop()
