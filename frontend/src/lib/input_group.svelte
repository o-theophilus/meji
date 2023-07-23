<script>
	import SVG from '$lib/comp/svg.svelte';

	export let name;
	export let label = '';
	export let svg = '';
	export let error = {};
	let id = name.split(' ').join('_');
</script>

<div class="inputGroup" class:svgi={!!svg}>
	<slot name="label" />
	{#if !$$slots.label}
		<label for={id}>{label || name}</label>
	{/if}
	{#if error[id]}
		<span class="error">
			{error[id]}
		</span>
	{/if}
	<slot {id} />
	{#if svg}
		<div class="svg">
			<SVG type={svg} size="20" />
		</div>
	{/if}
</div>
<br />

<style>
	.inputGroup {
		display: flex;
		flex-direction: column;
		gap: var(--sp1);
	}
</style>
