<script>
	import { module } from '$lib/store.js';

	import BRound from '$lib/button/round.svelte';
	import Form from './name_form.svelte';

	export let user = {};
	export let edit_mode = false;
</script>

<div class="row">
	<span class="name">
		{user.name}
	</span>
	{#if edit_mode}
		<BRound
			icon="edit"
			icon_size="10"
			tooltip="Edit Name"
			on:click={() => {
				$module = {
					module: Form,
					user: user
				};
			}}
		/>
	{/if}
</div>

<style>
	.name {
		font-weight: 900;
		color: var(--ac1);
	}

	.row {
		display: flex;
		gap: var(--sp1);
		align-items: center;
		flex-wrap: wrap;
		justify-content: space-between;
	}
</style>
