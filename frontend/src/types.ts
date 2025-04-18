// types.ts
export interface SubPlanFeature {
      id: number;
      title: string;
    }
    
    export interface SubPlan {
      id: number;
      title: string;
      price: number;
      features: SubPlanFeature[];
    }
    
    export interface UserProfile {
      id?: number;
      bio: string;
      first_name: string;
      last_name: string;
      location: string;
      profile_pic?: string;
    }