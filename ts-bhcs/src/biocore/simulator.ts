/**
 * BioCore Simulator - Abstract Biological Signal Modeling
 * 
 * Models plant compounds as signal sources and drugs as pathway modifiers.
 * Outputs synergy scores, not treatments.
 */

export interface PlantCompound {
    name: string;
    compounds: string[];
    potency: number;
    properties: {
        antiInflammatory: number;
        neuroprotective: number;
        immuneModulation: number;
        stressReduction: number;
    };
}

export interface DrugTarget {
    name: string;
    pathways: string[];
    effectiveness: number;
    toxicity: number;
}

export interface BioCoreEffect {
    id: string;
    zoneId: number;
    plant: string;
    drug: string;
    synergy: number;
    magnitude: number;
    effects: {
        calming: number;
        healing: number;
        protection: number;
    };
    timestamp: number;
}

export class BioCoreSimulator {
    private plants: Map<string, PlantCompound>;
    private drugs: Map<string, DrugTarget>;
    private activeEffects: Map<string, BioCoreEffect>;
    private effectHistory: BioCoreEffect[];

    constructor() {
        this.plants = new Map();
        this.drugs = new Map();
        this.activeEffects = new Map();
        this.effectHistory = [];
        
        this.initializePlants();
        this.initializeDrugs();
    }

    /**
     * Initialize plant database with abstract properties
     */
    private initializePlants(): void {
        const plantData: PlantCompound[] = [
            {
                name: 'Ginkgo',
                compounds: ['Ginkgolides', 'Flavonoids'],
                potency: 0.7,
                properties: {
                    antiInflammatory: 0.6,
                    neuroprotective: 0.8,
                    immuneModulation: 0.5,
                    stressReduction: 0.4
                }
            },
            {
                name: 'Aloe',
                compounds: ['Aloin', 'Acemannan'],
                potency: 0.5,
                properties: {
                    antiInflammatory: 0.8,
                    neuroprotective: 0.3,
                    immuneModulation: 0.6,
                    stressReduction: 0.2
                }
            },
            {
                name: 'Turmeric',
                compounds: ['Curcumin', 'Turmerone'],
                potency: 0.8,
                properties: {
                    antiInflammatory: 0.9,
                    neuroprotective: 0.6,
                    immuneModulation: 0.7,
                    stressReduction: 0.5
                }
            },
            {
                name: 'Ginseng',
                compounds: ['Ginsenosides'],
                potency: 0.6,
                properties: {
                    antiInflammatory: 0.5,
                    neuroprotective: 0.7,
                    immuneModulation: 0.8,
                    stressReduction: 0.6
                }
            },
            {
                name: 'Ashwagandha',
                compounds: ['Withanolides'],
                potency: 0.9,
                properties: {
                    antiInflammatory: 0.7,
                    neuroprotective: 0.8,
                    immuneModulation: 0.9,
                    stressReduction: 0.9
                }
            }
        ];

        plantData.forEach(plant => {
            this.plants.set(plant.name, plant);
        });
    }

    /**
     * Initialize drug database with abstract targets
     */
    private initializeDrugs(): void {
        const drugData: DrugTarget[] = [
            {
                name: 'DrugA',
                pathways: ['COX-2', '5-HT'],
                effectiveness: 0.6,
                toxicity: 0.1
            },
            {
                name: 'DrugB',
                pathways: ['NF-κB', 'MAO'],
                effectiveness: 0.7,
                toxicity: 0.15
            },
            {
                name: 'DrugC',
                pathways: ['NMDA', 'GABA'],
                effectiveness: 0.8,
                toxicity: 0.2
            },
            {
                name: 'DrugD',
                pathways: ['Dopamine', 'Serotonin'],
                effectiveness: 0.5,
                toxicity: 0.05
            },
            {
                name: 'DrugE',
                pathways: ['HPA-axis', 'Cortisol'],
                effectiveness: 0.9,
                toxicity: 0.25
            }
        ];

        drugData.forEach(drug => {
            this.drugs.set(drug.name, drug);
        });
    }

    /**
     * Initialize the simulator
     */
    public async initialize(): Promise<void> {
        console.log('🌿 BioCore Simulator: Plant and drug databases initialized');
    }

    /**
     * Update simulator with current zone states
     */
    public async update(zoneStates: any[]): Promise<void> {
        // Process active effects and decay over time
        for (const [effectId, effect] of this.activeEffects) {
            const age = Date.now() - effect.timestamp;
            const decayFactor = Math.exp(-age / 30000); // 30 second half-life
            
            if (decayFactor < 0.01) {
                this.activeEffects.delete(effectId);
            } else {
                effect.magnitude *= decayFactor;
                this.activeEffects.set(effectId, effect);
            }
        }
    }

    /**
     * Calculate BioCore effect for plant-drug combination
     */
    public calculateEffect(plantName: string, drugName: string, synergy: number): BioCoreEffect {
        const plant = this.plants.get(plantName);
        const drug = this.drugs.get(drugName);
        
        if (!plant || !drug) {
            throw new Error(`Unknown plant or drug: ${plantName}, ${drugName}`);
        }

        // Calculate abstract synergy score
        const pathwayCompatibility = this.calculatePathwayCompatibility(plant, drug);
        const baseSynergy = (plant.potency + drug.effectiveness) / 2;
        const finalSynergy = baseSynergy * pathwayCompatibility * synergy;

        // Calculate effect magnitudes
        const effects = {
            calming: (plant.properties.stressReduction * drug.effectiveness) * finalSynergy,
            healing: (plant.properties.antiInflammatory * drug.effectiveness) * finalSynergy,
            protection: (plant.properties.immuneModulation * drug.effectiveness) * finalSynergy
        };

        // Overall magnitude (homeostatic influence)
        const magnitude = (effects.calming + effects.healing + effects.protection) / 3;

        return {
            id: `${plantName}-${drugName}-${Date.now()}`,
            zoneId: -1, // Will be set when applied
            plant: plantName,
            drug: drugName,
            synergy: finalSynergy,
            magnitude,
            effects,
            timestamp: Date.now()
        };
    }

    /**
     * Calculate pathway compatibility between plant and drug
     */
    private calculatePathwayCompatibility(plant: PlantCompound, drug: DrugTarget): number {
        // Abstract compatibility calculation
        const plantScore = (
            plant.properties.antiInflammatory +
            plant.properties.neuroprotective +
            plant.properties.immuneModulation +
            plant.properties.stressReduction
        ) / 4;

        const drugScore = (drug.effectiveness + (1 - drug.toxicity)) / 2;

        return Math.min(1, (plantScore + drugScore) / 2);
    }

    /**
     * Get optimal BioCore recommendation for zone
     */
    public getOptimalForZone(zoneState: any): BioCoreEffect | null {
        let bestEffect: BioCoreEffect | null = null;
        let bestScore = -1;

        // Try all combinations
        for (const [plantName] of this.plants) {
            for (const [drugName] of this.drugs) {
                for (const synergy of [0.5, 0.7, 0.9]) {
                    const effect = this.calculateEffect(plantName, drugName, synergy);
                    
                    // Score based on zone needs
                    let score = 0;
                    if (zoneState.state === 'OVERSTIMULATED') {
                        score = effect.effects.calming * 2 + effect.effects.protection;
                    } else if (zoneState.state === 'EMERGENT') {
                        score = effect.effects.healing + effect.effects.protection;
                    } else {
                        score = effect.magnitude;
                    }

                    if (score > bestScore) {
                        bestScore = score;
                        bestEffect = effect;
                    }
                }
            }
        }

        return bestEffect;
    }

    /**
     * Record applied effect
     */
    public recordEffect(zoneId: number, plant: string, drug: string, synergy: number, effect: BioCoreEffect): void {
        effect.zoneId = zoneId;
        this.activeEffects.set(effect.id, effect);
        this.effectHistory.push(effect);
        
        // Keep history manageable
        if (this.effectHistory.length > 1000) {
            this.effectHistory = this.effectHistory.slice(-500);
        }

        console.log(`🌿 BioCore effect recorded: Zone ${zoneId}, ${plant} + ${drug}`);
    }

    /**
     * Get currently active effects
     */
    public getActiveEffects(): BioCoreEffect[] {
        return Array.from(this.activeEffects.values());
    }

    /**
     * Get effect history
     */
    public getEffectHistory(): BioCoreEffect[] {
        return [...this.effectHistory];
    }

    /**
     * Get analytics data
     */
    public getAnalytics() {
        const history = this.effectHistory;
        if (history.length === 0) return null;

        const plantUsage = new Map<string, number>();
        const drugUsage = new Map<string, number>();
        let totalSynergy = 0;

        history.forEach(effect => {
            plantUsage.set(effect.plant, (plantUsage.get(effect.plant) || 0) + 1);
            drugUsage.set(effect.drug, (drugUsage.get(effect.drug) || 0) + 1);
            totalSynergy += effect.synergy;
        });

        return {
            totalEffects: history.length,
            averageSynergy: totalSynergy / history.length,
            mostUsedPlant: this.getMostUsed(plantUsage),
            mostUsedDrug: this.getMostUsed(drugUsage),
            topCombinations: this.getTopCombinations()
        };
    }

    /**
     * Get most used item from usage map
     */
    private getMostUsed(usage: Map<string, number>): string | null {
        let maxUsage = 0;
        let mostUsed = null;

        for (const [item, count] of usage) {
            if (count > maxUsage) {
                maxUsage = count;
                mostUsed = item;
            }
        }

        return mostUsed;
    }

    /**
     * Get top performing combinations
     */
    private getTopCombinations(): Array<{plant: string, drug: string, avgSynergy: number}> {
        const combinations = new Map<string, {count: number, totalSynergy: number}>();

        this.effectHistory.forEach(effect => {
            const key = `${effect.plant}-${effect.drug}`;
            const existing = combinations.get(key) || {count: 0, totalSynergy: 0};
            combinations.set(key, {
                count: existing.count + 1,
                totalSynergy: existing.totalSynergy + effect.synergy
            });
        });

        return Array.from(combinations.entries())
            .map(([key, data]) => {
                const [plant, drug] = key.split('-');
                return {
                    plant,
                    drug,
                    avgSynergy: data.totalSynergy / data.count
                };
            })
            .sort((a, b) => b.avgSynergy - a.avgSynergy)
            .slice(0, 5);
    }

    /**
     * Reset simulator
     */
    public reset(): void {
        this.activeEffects.clear();
        this.effectHistory = [];
        console.log('🔄 BioCore Simulator reset');
    }
}
