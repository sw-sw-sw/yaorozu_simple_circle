# queueの種類

プロセス間ごとに設定する。

## Ecosystem <..> VisualSystem 

add_agent(position, agent_id, agent_species) -> agent_radius:
remove_agent(agent_id) -> step complete:

## DeathEffect ..> Ecosystem

death_effect_finished(agent_id) -> True

## Ecosystem <..>Box2dSimulation

create_agent (positions, velocity, agent species, agent_id, agent_radius)-> step complete
remove agent(agent_id) -> step complete