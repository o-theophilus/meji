<script>
	import { slide } from 'svelte/transition';
	import { backInOut } from 'svelte/easing';

	import { createEventDispatcher } from 'svelte';

	import { page_name, state } from '$lib/page_state.js';

	import Button from '$lib/comp/button.svelte';
	import View from './page_item_view.svelte';

	let emit = createEventDispatcher();

	export let show_view;

	let input_order = ['date', 'name', 'price', 'discount'];
	// 'rating'

	let order = $state[$page_name].order;
	let order_dir = $state[$page_name].order_dir;

	const direct = () => {
		order_dir = order_dir == 'asc' ? 'dsc' : 'asc';
	};
	const submit = () => {
		$state[$page_name].order = order;
		$state[$page_name].order_dir = order_dir;
		emit('ok');
	};
</script>

{#if show_view}
	<section transition:slide|local={{ delay: 0, duration: 200, easing: backInOut }}>
		<View />

		|
		<label>
			order:
			<select bind:value={order}>
				{#each input_order as value}
					<option {value}>
						{value}
					</option>
				{/each}
			</select>
			|
		</label>
		<div class="dir" on:click={direct}>{order_dir == 'asc' ? '↓' : '↑'}</div>

		<Button
			name="Ok"
			class="tiny"
			on:click={() => {
				submit();
			}}
		/>
	</section>
{/if}

<style>
	* {
		color: var(--font1);
	}

	section {
		display: flex;
		justify-content: flex-end;
		align-items: center;

		gap: var(--gap2);

		padding: var(--gap2);
		/* border-top: 2px solid var(--background); */

		color: var(--font1);
		/* background-color: var(--background); */
	}

	select {
		background-color: var(--foreground);
		border: none;
	}

	.dir {
		cursor: pointer;
		padding: var(--gap1);
	}
</style>
