<script>
	import { slide } from 'svelte/transition';
	import { backInOut } from 'svelte/easing';
	import { state } from '$lib/store.js';
	import { user } from '$lib/store.js';

	import Button from '$lib/button.svelte';

	let input_order = ['date', 'name', 'price', 'discount']; // 'rating'

	let order = '';
	let order_dir = '';

	const direct = () => {
		// order_dir = order_dir == 'asc' ? 'dsc' : 'asc';
	};
	const eee = () => {
		//wewe
	};

	export let page_name = '';
	let item_view = 'grid';
	if ($user) {
		item_view = $user.setting.item_view;
	}
</script>

<section transition:slide|local={{ delay: 0, duration: 200, easing: backInOut }}>
	<div on:click={submit}>{item_view}</div>

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
			eee();
		}}
	/>
</section>

<style>
	* {
		color: var(--ac1);
	}

	section {
		display: flex;
		/* justify-content: flex-end; */
		align-items: center;
		gap: var(--sp2);

		/* margin-top: var(--sp2); */

		color: var(--ac1);
	}

	select {
		background-color: var(--ac4);
		border: none;
	}

	.dir {
		cursor: pointer;
		padding: var(--sp1);
	}
</style>
