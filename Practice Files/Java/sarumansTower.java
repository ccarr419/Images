public class sarumansTower {

    public static void main(String[] args) {
        // TODO code application logic here
        int day[] = {2, 19, 64};
        int lvl[] = new int[3];
        for(int i = 0; i < 3; i++)
            lvl[i] = findLevels(day[i]);
        
        for(int i = 0; i < 3; i++)
            System.out.println("Day " + day[i] + ": Level = " + lvl[i]);
    }
    
    public static int findLevels(int end_day) {
        if(end_day < 7)
            return 0;
        
        int count[] = {0};
        int day = 7, lvl = 0;
        while(day <= end_day) {
            int num[] = toBinary(count, day, day-1);
            if(num[0] != 0 && num[0] % 3 == 0)
                lvl++;
            day++;
        }
        return lvl;
    }
    
    public static int[] toBinary(int count[], double num, double k) {
        if(num == 0 || k < 0)
            return count;
        
        if(Math.pow(2, k) <= num) {
            count[0] += 1;
            toBinary(count, num-Math.pow(2, k), k-1);
        }            
        
        else
            toBinary(count, num, k-1); 
        
        return count;
    }
}
