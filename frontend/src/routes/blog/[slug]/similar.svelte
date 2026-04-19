<script>
	import { FoldButton } from '$lib/button';
	import { Content } from '$lib/layout';
	import { Avatar, Spinner } from '$lib/macro';
	import { app } from '$lib/store.svelte.js';
	import { cubicInOut } from 'svelte/easing';
	import { slide } from 'svelte/transition';

	let { similar = [], loading } = $props();
	let open = $state(true);

	const prerender = (blog) => {
		app.blog = blog;
	};
</script>

{#if loading || similar.length}
	<Content --content-background-color="var(--bg2)" --content-height="auto">
		<div class="title line">
			<div class="page_title line">
				Similar Blog{#if similar.length > 1}s{/if}
				<Spinner active={loading} size="20" />
			</div>

			{#if !loading}
				<FoldButton
					{open}
					onclick={() => {
						open = !open;
					}}
				/>
			{/if}
		</div>

		{#if open && !loading}
			<div class="area" transition:slide|local={{ delay: 0, duration: 200, easing: cubicInOut }}>
				{#each similar as blog}
					<div class="one">
						<a
							href="/blog/{blog.slug}"
							onclick={() => prerender(blog)}
							onmouseenter={() => prerender(blog)}
						>
							<Avatar size="58" photo={blog.photo} no_photo="/no_photo.png" name={blog.title}
							></Avatar>
						</a>
						<div class="details">
							<a
								class="link"
								href="/blog/{blog.slug}"
								onclick={() => {
									prerender(blog);
									update(blog);
								}}
								onmouseenter={() => prerender(blog)}
							>
								{blog.title}
							</a>

							{#if blog.description}
								<br />
								<div class="desc">
									{blog.description}
								</div>
							{/if}
						</div>
					</div>
				{/each}
			</div>
		{/if}
	</Content>
{/if}

<style>
	.title {
		justify-content: space-between;
	}

	.area {
		display: grid;
		gap: 24px;
		margin-top: 24px;

		@media screen and (min-width: 600px) {
			& {
				grid-template-columns: 1fr 1fr;
			}
		}
	}

	.one {
		display: flex;
		gap: 16px;

		& .link {
			text-decoration: none;
			color: var(--link-color, var(--link));
			font-weight: 700;

			line-height: 10%;

			transition: color 0.2s ease-in-out;

			&:hover {
				color: var(--link-color-hover, color-mix(in srgb, var(--link), black 30%));
			}
		}

		& .desc {
			margin-top: 4px;
			font-size: 0.7rem;
		}
	}
</style>
