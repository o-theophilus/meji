<script>
	import Center from '$lib/center.svelte';

	export let size = '300x300';
	export let adverts = [];

	let index = 0;

	const auto_scroll = () => {
		index += 1;
		if (index > adverts.length - 1) {
			index = 0;
		}
	};

	let timer = setInterval(auto_scroll, 1000 * 5);
	const reset_timer = () => {
		clearInterval(timer);
		timer = setInterval(auto_scroll, 1000 * 5);
	};
</script>

{#if adverts.length > 0}
	<Center>
		<section>
			<a href="/{adverts[index].item.key}">
				<img src={adverts[index].photos[size]} alt={adverts[index].item.name} />
			</a>

			{#if adverts.length > 1}
				<div class="control">
					{#each adverts as _, i}
						<div
							class="btn"
							class:active={index == i}
							on:keypress
							role="button"
							tabindex="0"
							on:click={() => {
								index = i;
								reset_timer();
							}}
						/>
					{/each}
				</div>
			{/if}
		</section>
	</Center>
{/if}

<style>
	section {
		display: flex;
		position: relative;
		box-shadow: var(--shad1);
		border-radius: var(--sp0);
		overflow: hidden;
	}

	a {
		display: flex;
		width: 100%;
	}
	img {
		width: 100%;
		cursor: pointer;
	}

	.control {
		position: absolute;
		bottom: 24px;

		display: flex;
		gap: var(--sp1);
		justify-content: center;

		width: 100%;
	}

	.btn {
		--size: 20px;

		width: var(--size);
		height: var(--size);

		border-radius: var(--size);

		background-color: var(--cl1);

		transition: var(--trans1);
	}

	.btn:hover {
		width: calc(var(--size) * 2.5);
	}

	.btn.active {
		width: calc(var(--size) * 2.5);
	}
</style>
