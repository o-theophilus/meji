<script>
	import { page } from '$app/stores';
	import { onMount } from 'svelte';
	import { set_state } from '$lib/store.js';
	import Button from '$lib/button.svelte';

	let page_no, page_no_temp, width;
	export let total_page = 1;
	export let page_name = '';

	const normalise = (value) => {
		if (value < 1) {
			value = 1;
		} else if (value > total_page) {
			value = total_page;
		}
		return value;
	};

	onMount(() => {
		let params = $page.url.searchParams;
		if (params.has('page_no')) {
			page_no = page_no_temp = normalise(params.get('page_no'));
		}
	});

	const submit = (value) => {
		value = normalise(value);
		page_no = page_no_temp = value;
		set_state(page_name, 'page_no', value != 1 ? value : '');
	};

	$: {
		total_page;
		page_no = page_no_temp = 1;
	}
</script>

{#if total_page > 1}
	<section>
		{#if page_no > 1}
			<Button
				class="tiny"
				name="❮ prev"
				on:click={() => {
					submit(page_no - 1);
				}}
			/>
		{/if}

		<div class="input">
			<input
				style:width="{width}px"
				type="text"
				oninput="this.value = this.value.replace(/[^0-9]/g, '')"
				bind:value={page_no_temp}
				on:keypress={(e) => {
					if (e.key == 'Enter') {
						submit(page_no_temp);
					}
				}}
			/>
			<div class="total">
				/ {total_page}
			</div>
		</div>

		<div class="width_helper" bind:clientWidth={width}>
			<span>
				{#if page_no_temp}
					{page_no_temp}
				{:else}
					0
				{/if}
			</span>
			// {total_page}
		</div>

		{#if page_no_temp != page_no}
			<Button
				class="tiny"
				name="go ❯❯"
				on:click={() => {
					submit(page_no_temp);
				}}
			/>
		{/if}

		{#if page_no < total_page}
			<Button
				class="tiny"
				name="next ❯"
				on:click={() => {
					submit(parseInt(page_no) + 1);
				}}
			/>
		{/if}
	</section>
{/if}

<style>
	section {
		display: flex;
		justify-content: center;
		gap: var(--sp1);

		margin: var(--sp2);
	}

	.input {
		position: relative;
		display: flex;
		align-items: center;
		justify-content: center;
	}
	input {
		border: 2px solid var(--ac3);
	}

	.total {
		position: absolute;
		right: var(--sp2);
		pointer-events: none;
		color: var(--ac2);
	}

	.width_helper {
		position: absolute;
		visibility: hidden;
		padding: var(--sp2);
		display: inline-block;
	}
</style>
