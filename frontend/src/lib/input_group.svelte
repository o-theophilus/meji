<script>
	export let name;
	export let label = '';
	export let error = {};
	let id = name.split(' ').join('_').toLowerCase();
</script>

<div class="inputGroup">
	<slot name="label" />
	{#if !$$slots.label}
		<label for={id}>{label || name.replace(/_/g, ' ')}</label>
	{/if}
	{#if error[id]}
		<span class="error">
			{error[id]}
		</span>
	{/if}
	<slot {id} />
</div>
<br />

<style>
	.inputGroup {
		display: flex;
		flex-direction: column;
		gap: var(--sp1);
	}
</style>
