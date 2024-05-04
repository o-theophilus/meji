<script>
	import { user, module } from '$lib/store.js';

	import BRound from '$lib/button/round.svelte';
	import SVG from '$lib/svg.svelte';
	import Save from '$lib/item/save.svelte';
	import Form from './name_form.svelte';

	export let item = {};
	export let edit_mode = false;
</script>

<div class="horizontal">
	<span class="name">{item.name} </span>

	<div class="horizontal">
		<Save {item} />

		{#if edit_mode && $user.permissions.includes('item:edit_name')}
			<BRound
				on:click={() => {
					$module = {
						module: Form,
						item
					};
				}}
				tooltip="Edit Name"
			>
				<SVG type="edit" size="10" />
			</BRound>
		{/if}
	</div>
</div>

<style>
	.horizontal {
		display: flex;
		justify-content: space-between;
		gap: var(--sp1);
		align-items: center;
		flex-wrap: wrap;
	}

	.name {
		color: var(--ac1);
		text-transform: capitalize;
		font-weight: 900;
	}
</style>
