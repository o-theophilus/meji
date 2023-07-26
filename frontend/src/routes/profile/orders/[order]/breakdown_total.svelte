<script>
	import { createEventDispatcher } from 'svelte';
	let emit = createEventDispatcher();

	export let title;
	export let value;
	export let u_title = false;
	export let u_value = false;
</script>

<section>
	<div
		class="title"
		class:u={u_title}
		on:click={() => {
			emit('title');
		}}
	>
		{title}
	</div>
	<div
		class="value"
		class:u={u_value}
		on:click={() => {
			emit('value');
		}}
	>
		₦{value.toLocaleString()}
	</div>
</section>

<style>
	section {
		display: flex;
		gap: var(--sp3);
		font-weight: 500;
		justify-content: right;

		text-align: right;
	}

	.value {
		min-width: 3em;
	}

	.u {
		text-decoration: underline;
		cursor: pointer;
	}
</style>
