# Decisions:

1. It was decided to make individual scraping function for every object instead of one function for all objects so as
   to make possible for one scraping function to fail without this resulting in not getting any object of this type.
   With this it is possible to catch this individual error and still continue with the rest of the obejcts of this type.
   But this behavior is only desireable for an object as a whole not for parts of an object like updates for an 
   incident.