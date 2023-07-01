<script>
	import { createEventDispatcher } from 'svelte';
	import { loading } from '$lib/store.js';
	import { state, page_name } from '$lib/page_state.js';

	import Body from '$lib/comp/card_body.svelte';
	import Button from '$lib/comp/button.svelte';

	let emit = createEventDispatcher();

	export let total_page;
	let value = $state[$page_name].page_no;

	const goto_page = async (p) => {
		if (p < 1) {
			p = 1;
		} else if (p > total_page) {
			p = total_page;
		}

		$state[$page_name].page_no = p;
		value = p;
		emit('ok');
	};

	export const init = async () => {
		$state[$page_name].page_no = 1;
		value = 1;
	};

	let width;
	let width2;
</script>

{#if total_page > 1}
	<Body>
		<section class:loading={$loading}>
			{#if $state[$page_name].page_no > 1}
				<Button
					name="❮ prev"
					class="link"
					color="var(--font2)"
					on:click={() => {
						goto_page($state[$page_name].page_no - 1);
					}}
				/>
			{/if}

			<div class="input">
				<span class="helper" bind:clientWidth={width}>
					{value}
				</span>
				<input
					style:width="calc({width}px + {width2}px)"
					size="0"
					type="number"
					bind:value
					on:keypress={(e) => {
						if (e.key == 'Enter') {
							goto_page(value);
						}
					}}
				/>
				<div class="total" bind:clientWidth={width2}>
					of {total_page}
				</div>
			</div>

			{#if $state[$page_name].page_no != value}
				<Button
					name="go ❯❯"
					class="link"
					color="var(--font2)"
					on:click={() => {
						goto_page(value);
					}}
				/>
			{/if}

			{#if $state[$page_name].page_no < total_page}
				<Button
					name="next ❯"
					class="link"
					color="var(--font2)"
					on:click={() => {
						goto_page($state[$page_name].page_no + 1);
					}}
				/>
			{/if}
		</section>
	</Body>
{/if}

<style>
	section {
		display: flex;
		justify-content: center;
		gap: var(--gap1);
	}
	.loading {
		opacity: 0.5;
	}

	.input {
		position: relative;
		display: flex;
		align-items: center;
	}

	input {
		padding: var(--gap1);

		background: transparent;
		font-weight: 500;
		margin-right: 2px;

		border-radius: var(--brad1);
		border: 2px solid var(--background);

		color: var(--font1);
	}

	input:hover {
		border-color: var(--midtone);
	}
	input:focus {
		border-color: var(--color1);
	}
	.total {
		position: absolute;
		right: calc(var(--gap1) + 4px);
		pointer-events: none;
		font-size: small;
	}

	.helper {
		position: absolute;
		visibility: hidden;

		padding: calc(var(--gap1) + 4px);
	}
</style>
