import { v4 as uuidv4 } from 'uuid';

export class UnitSystem {
  constructor(eventBus) {
    this.units = new Map();
    this.eventBus = eventBus;
    this.setupEventListeners();
  }

  setupEventListeners() {
    this.eventBus.on('external-input', this.handleExternalInput.bind(this));
    this.eventBus.on('unit-mutation', this.handleUnitMutation.bind(this));
  }

  createUnit(type, properties = {}) {
    const unit = {
      id: uuidv4(),
      type,
      properties,
      created: Date.now(),
      fitness: 0,
      generation: 1
    };
    
    this.units.set(unit.id, unit);
    this.eventBus.emit('unit-created', unit);
    return unit;
  }

  handleExternalInput(data) {
    // Process external input and potentially create new units
    if (data.type === 'create-unit') {
      this.createUnit(data.unitType, data.properties);
    }
  }

  handleUnitMutation(unitId) {
    const unit = this.units.get(unitId);
    if (!unit) return;

    // Implement mutation logic
    const mutatedProperties = this.mutateProperties(unit.properties);
    unit.properties = mutatedProperties;
    unit.generation++;
    
    this.eventBus.emit('system-update', {
      type: 'unit-mutated',
      unit
    });
  }

  mutateProperties(properties) {
    // Basic mutation implementation
    return {
      ...properties,
      mutationCount: (properties.mutationCount || 0) + 1,
      lastMutation: Date.now()
    };
  }
}