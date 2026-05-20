<script>
	import { Datetime } from '$lib/macro';
	let { data } = $props();

	for (let log of data) {
		log.href = '';
		if (!log.entity) {
			log.href = '';
		} else if (log.entity.type == 'item') {
			log.href = `/${log.entity.slug}`;
			if (log.action == 'added comment to item') {
				log.href = `/${log.entity.slug}/review#${log.misc.comment_key}`;
			}
		} else if (log.entity.type == 'blog') {
			log.href = `/blog/${log.entity.slug}`;
			if (log.action == 'added comment to blog') {
				log.href = `/blog/${log.entity.slug}#${log.misc.comment_key}`;
			}
		} else if (log.entity.type == 'user') {
			log.href = `/@${log.entity.slug}`;
		} else if (log.entity.type == 'page') {
			log.href = log.entity.slug;
		}
	}
</script>

{#each data as log}
	<section>
		<div
			class="status"
			class:_200={log.status == '200'}
			class:_201={!['200', '400'].includes(log.status)}
			class:_400={log.status == '400'}
		></div>

		<span class="date">
			<Datetime datetime={log.date_created} type="date_numeric" />
			<Datetime datetime={log.date_created} type="time_12h" />
		</span>
		:

		{#if log.user}
			<a href="/@{log.user.username}" class="break">
				{log.user.name}
			</a>
		{/if}

		{log.action}

		{#if log.href}
			<a class="break" href={log.href} data-sveltekit-preload-data="off">
				{log.entity.name}
			</a>
		{/if}
	</section>
{/each}

<style>
	section {
		margin-top: 8px;
		font-size: 0.8rem;
	}

	.status {
		display: inline-block;
		display: none;
		--size: 10px;
		width: var(--size);
		height: var(--size);

		border-radius: 50%;
		color: var(--ac6_);
	}
	._200 {
		background-color: green;
	}
	._201 {
		background-color: var(--yellow);
	}
	._400 {
		background-color: red;
	}

	.date {
		font-size: 0.7rem;
		font: italic;
	}

	a {
		color: var(--cl1);
		text-decoration: none;
		font-weight: 700;

		&:hover {
			color: var(--cl1_b);
		}
	}

	.break {
		word-wrap: break-word;
	}
</style>
