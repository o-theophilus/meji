<script>
	import { page } from '$app/stores';
	import { onMount } from 'svelte';
	import { set_state } from '$lib/store.js';

	let _page_no, page_no, width;
	export let total_page = 1;
	export let page_name;

	const normalize = (x) => {
		if (x < 1) {
			x = 1;
		} else if (x > total_page) {
			x = total_page;
		}
		return x;
	};

	const submit = (value) => {
		value = normalize(value);
		_page_no = page_no = value;
		set_state(page_name, 'page_no', value != 1 ? value : '');
	};

	let set_page_no = () => {
		if ($page.url.searchParams.has('page_no')) {
			_page_no = page_no = normalize($page.url.searchParams.get('page_no'));
		} else {
			_page_no = page_no = 1;
		}
	};
	onMount(() => {
		set_page_no();
	});

	$: {
		$page.url;
		set_page_no();
	}
</script>

{#if total_page > 1}
	<br />
	<br />

	<section>
		{#if _page_no > 1}
			<button
				on:click={() => {
					submit(_page_no - 1);
				}}
			>
				&lt;
			</button>
		{/if}

		<div class="input">
			<input
				style:width="calc({width}px + 4px)"
				type="text"
				oninput="this.value = this.value.replace(/[^0-9]/g, '')"
				bind:value={page_no}
				on:keypress={(e) => {
					if (e.key == 'Enter') {
						submit(page_no);
					}
				}}
			/>
			<div class="total">
				/ {total_page}
			</div>
		</div>

		<div class="width_helper" bind:clientWidth={width}>
			<span>
				{#if page_no}
					{page_no}
				{:else}
					0
				{/if}
			</span>
			/ {total_page}
		</div>

		{#if page_no != _page_no}
			<button
				on:click={() => {
					submit(page_no);
				}}
			>
				&gt;&gt;
			</button>
		{/if}

		{#if _page_no < total_page}
			<button
				on:click={() => {
					submit(parseInt(_page_no) + 1);
				}}
			>
				&gt;
			</button>
		{/if}
	</section>
{/if}

<style>
	section {
		--size: var(--sp1);
		--height: 40px;

		display: flex;

		width: fit-content;
		margin: auto;
		border-radius: var(--sp0);
		overflow: hidden;

		color: var(--ac3);
		outline: 2px solid var(--ac4);
	}
	section:hover {
		outline-color: var(--ac3);
	}
	section:has(input:focus) {
		outline-color: var(--ac1);
	}

	.input {
		position: relative;
		display: flex;
		align-items: center;
		justify-content: center;
	}
	input {
		padding: var(--size);
		height: var(--height);
		border: none;

		color: var(--ac1);
		background-color: var(--ac5);
	}

	.total {
		position: absolute;
		right: var(--size);
		pointer-events: none;
	}

	.width_helper {
		position: absolute;
		visibility: hidden;
		padding: var(--size);
		display: inline-block;
	}

	button {
		aspect-ratio: 1/1;
		height: var(--height);

		background-color: var(--ac6);
		color: var(--ac2);
		border: none;
		cursor: pointer;
		font-weight: 700;
	}

	button:hover {
		background-color: var(--cl1_b);
		color: var(--ac6_);
	}
</style>
