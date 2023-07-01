<script>
	import { createEventDispatcher } from 'svelte';
	import { user } from '$lib/store.js';
	import { state, page_name } from '$lib/page_state.js';

	import Button from '$lib/comp/button.svelte';

	export let bar_items = [];
	export let query = 'status';

	let emit = createEventDispatcher();
	const submit = (status) => {
		$state[$page_name][query] = status;
		emit('ok');
	};
</script>

<div class="block">
	<div class="base">
		<slot name="before" />
		{#each bar_items as status}
			<Button
				name={status.name}
				icon={status.icon}
				class="tiny"
				active={status.name == $state[$page_name][query]}
				on:click={() => {
					submit(status.name);
				}}
			/>
		{/each}
	</div>
	<div class="after">
		<slot name="after" />
	</div>
</div>

<style>
	.block {
		display: flex;
		gap: var(--gap1);

		padding: var(--gap1) var(--gap2);
		border-top: 2px solid var(--background);
	}
	.base {
		display: flex;
		gap: var(--gap1);
		flex-wrap: wrap;
	}

	.after {
		margin-left: auto;
	}
</style>
