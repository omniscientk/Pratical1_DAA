#include <iostream>
#include <vector>

// Function to perform Bubble Sort
void bubbleSort(std::vector<int>& arr) {
    int n = arr.size();
    bool swapped;
    
    for (int i = 0; i < n - 1; ++i) {
        swapped = false;
        
        // Last i elements are already in place
        for (int j = 0; j < n - i - 1; ++j) {
            if (arr[j] > arr[j + 1]) {
                // Swap if the element found is greater than the next element
                std::swap(arr[j], arr[j + 1]);
                swapped = true;
            }
        }
        
        // If no two elements were swapped by inner loop, then break
        if (!swapped) {
            break;
        }
    }
}

// Function to print the array
void printArray(const std::vector<int>& arr) {
    for (int num : arr) {
        std::cout << num << " ";
    }
    std::cout << std::endl;
}

int main() {
    std::vector<int> data = {64, 34, 25, 12, 22, 11, 90};
    
    std::cout << "Unsorted array: ";
    printArray(data);
    
    bubbleSort(data);
    
    std::cout << "Sorted array:   ";
    printArray(data);
    
    return 0;
}
