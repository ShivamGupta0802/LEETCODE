class Solution {
    public List<Boolean> kidsWithCandies(int[] candies, int extraCandies) {
        List<Boolean> result = new ArrayList<>();
        int max = Integer.MIN_VALUE;
        int i = 0;
        while (i < candies.length) {
            if (candies[i] > max) {
                max = candies[i];

            }
            i++;
        }
        i = 0;
        while (i < candies.length) {
            if (candies[i] + extraCandies >= max) {
                result.add(true);
            }else{
                result.add(false);
            }
            i++;
        }
        return result;
    }
}


// ### Array (`boolean[]`) vs List (`List<Boolean>`)

// - **Array method:** `boolean[] result = new boolean[n];`
//   - Fixed size; access or update using `result[i]`.
//   - Example: `result[i] = true;`
//   - Returns using `return result;`

// - **List method:** `List<Boolean> result = new ArrayList<>();`
//   - Dynamic size; add elements using `result.add(value)`.
//   - Example: `result.add(true);`
//   - Returns using `return result;`

// **Key difference:** `boolean[]` is an array of primitive `boolean` values, while `List<Boolean>` stores `Boolean` objects and supports methods like `.add()`.

// **LeetCode tip:** Always match the required return type in the method signature. If it says `List<Boolean>`, you must return a List, not an array.