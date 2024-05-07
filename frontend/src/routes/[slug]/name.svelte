<script>
	import { user, module } from '$lib/store.js';

	import BRound from '$lib/button/round.svelte';
	import ButtonFold from '$lib/button/fold.svelte';
	import Save from '$lib/item/save.svelte';
	import Form from './name_form.svelte';

	export let item = {};
	export let edit_mode = false;
	let open = item.tags.length > 0;
</script>

<div class="row space v_margin">
	<span class="bold">{item.name} </span>

	<div class="row">
		<ButtonFold
			{open}
			on:click={() => {
				open = !open;
			}}
		/>
		<Save {item} />

		{#if edit_mode && $user.permissions.includes('item:edit_name')}
			<BRound
				icon="edit"
				icon_size="10"
				tooltip="Edit Name"
				on:click={() => {
					$module = {
						module: Form,
						item
					};
				}}
			/>
		{/if}
	</div>
</div>

<slot {open} />

<style>
	.row {
		display: flex;
		gap: var(--sp1);
		align-items: flex-end;
	}

	.space {
		justify-content: space-between;
	}

	.v_margin {
		margin: var(--sp1) 0;
	}

	.bold {
		color: var(--ac1);
		text-transform: capitalize;
		font-weight: 900;
	}
</style>
