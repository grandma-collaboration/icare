import { useEffect, useState, useRef } from "react";
import { Chip, Tooltip } from "@mui/material";
import { getContrastColor } from "../ObjectTags";
import { useGetTagOptionsQuery } from "../../ducks/objectTags";

interface DynamicTagDisplayProps {
  source: { tags?: any[]; classifications?: any[] };
  styles: Record<string, string>;
  displayTags?: boolean;
  taxonomyList?: any[];
}

interface ChipTag {
  id: string | number;
  name: string;
  objtagoption_id?: number;
  chipClass: string;
  priority: number;
}

const confirmed_classes = [
  "Kilonova",
  "GRB",
  "GW Counterpart",
  "GW Candidate",
  "Supernova",
];
const rejected_classes = [
  "Not Kilonova",
  "Not GRB",
  "Not GW Counterpart",
  "Not GW Candidate",
  "Not Supernova",
];
const DynamicTagDisplay = ({
  source,
  styles,
  displayTags = true,
  taxonomyList = [],
}: DynamicTagDisplayProps) => {
  const [visibleTagsCount, setVisibleTagsCount] = useState(2);
  const [containerWidth, setContainerWidth] = useState(0);
  const containerRef = useRef<HTMLDivElement>(null);
  const measureRef = useRef<HTMLSpanElement>(null);

  const getGrandmaClassifications = (): ChipTag[] => {
    if (!source.classifications || !Array.isArray(source.classifications)) {
      return [];
    }

    const classifications: ChipTag[] = [];
    const source_status_taxonomy = taxonomyList?.find(
      (t: any) => t.name === "Grandma Campaign Source Classification",
    );
    const source_obs_taxonomy = taxonomyList?.find(
      (t: any) => t.name === "Grandma Campaign Source Observation",
    );

    const filteredClasses = source.classifications.filter(
      (i: any) => i && i.probability > 0,
    );
    const sortedClasses = filteredClasses.sort((a: any, b: any) =>
      a.modified < b.modified ? 1 : -1,
    );

    if (sortedClasses.length > 0) {
      if (source_status_taxonomy) {
        const grandmaStatusClass = sortedClasses.find(
          (c: any) => c && c.taxonomy_id === source_status_taxonomy.id,
        );
        if (grandmaStatusClass && grandmaStatusClass.classification) {
          let chipClass = "not_confirmed";
          if (rejected_classes.includes(grandmaStatusClass.classification)) {
            chipClass = "rejected";
          } else if (
            confirmed_classes.includes(grandmaStatusClass.classification)
          ) {
            chipClass = "confirmed";
          }

          classifications.push({
            id: `status_${grandmaStatusClass.id}`,
            name: grandmaStatusClass.classification,
            chipClass,
            priority: 1,
          });
        }
      }

      if (source_obs_taxonomy) {
        const grandmaObsClass = sortedClasses.find(
          (c: any) => c && c.taxonomy_id === source_obs_taxonomy.id,
        );
        if (grandmaObsClass && grandmaObsClass.classification) {
          let chipClass: string | null = null;
          if (
            grandmaObsClass.classification === "GO GRANDMA" ||
            grandmaObsClass.classification === "GO GRANDMA (HIGH PRIORITY)"
          ) {
            chipClass = "go";
          } else if (grandmaObsClass.classification === "STOP GRANDMA") {
            chipClass = "stop";
          }

          if (chipClass) {
            classifications.push({
              id: `obs_${grandmaObsClass.id}`,
              name: grandmaObsClass.classification,
              chipClass,
              priority: 2,
            });
          }
        }
      }
    }

    return classifications;
  };
  const { data: tagOptions = [] } = useGetTagOptionsQuery();

  const measureTextWidth = (text: string) => {
    if (!measureRef.current) return 0;

    // Temporary element to calculate the space it takes
    const tempElement = document.createElement("span");
    tempElement.style.visibility = "hidden";
    tempElement.style.position = "absolute";
    tempElement.style.whiteSpace = "nowrap";
    tempElement.style.fontSize = "0.8125rem";
    tempElement.style.fontFamily = window.getComputedStyle(
      measureRef.current,
    ).fontFamily;
    tempElement.style.padding = "4px 12px";
    tempElement.textContent = text;

    document.body.appendChild(tempElement);
    const width = tempElement.offsetWidth + 8;
    document.body.removeChild(tempElement);

    return width;
  };

  // Calculate how many tags we can put on the container
  const calculateVisibleTags = () => {
    const grandmaClassifications = getGrandmaClassifications();
    const tags: ChipTag[] = (source.tags || []).map((tag: any) => ({
      id: tag.id,
      name: tag.name,
      objtagoption_id: tag.objtagoption_id,
      chipClass: "default",
      priority: 3,
    }));

    const allTags: ChipTag[] = [...grandmaClassifications, ...tags];
    const uniqueTags: ChipTag[] = [];
    const seenNames = new Set<string>();

    allTags.sort((a, b) => a.priority - b.priority);
    allTags.forEach((tag) => {
      if (!seenNames.has(tag.name.toLowerCase())) {
        seenNames.add(tag.name.toLowerCase());
        uniqueTags.push(tag);
      }
    });

    if (uniqueTags.length === 0 || !containerRef.current) {
      return uniqueTags.length;
    }

    const availableWidth = containerRef.current.offsetWidth;
    let totalWidth = 0;
    let visibleCount = 0;

    for (let i = 0; i < uniqueTags.length; i++) {
      const tagWidth = measureTextWidth(uniqueTags[i]!.name);

      const remainingTags = uniqueTags.length - i;
      const needsPlusChip = remainingTags > 1;
      const plusChipWidth = needsPlusChip
        ? measureTextWidth(`+${remainingTags - 1}`)
        : 0;

      if (totalWidth + tagWidth + plusChipWidth <= availableWidth) {
        totalWidth += tagWidth;
        visibleCount++;
      } else {
        break;
      }
    }

    return Math.max(1, Math.min(visibleCount, uniqueTags.length));
  };

  useEffect(() => {
    if (!containerRef.current) return;

    const resizeObserver = new ResizeObserver((entries) => {
      for (const entry of entries) {
        const newWidth = entry.contentRect.width;
        if (newWidth !== containerWidth) {
          setContainerWidth(newWidth);
        }
      }
    });

    resizeObserver.observe(containerRef.current);

    return () => {
      resizeObserver.disconnect();
    };
  }, [containerWidth]);

  useEffect(() => {
    if (containerWidth > 0 && source.tags) {
      const newVisibleCount = calculateVisibleTags();
      setVisibleTagsCount(newVisibleCount);
    }
  }, [containerWidth, source.tags, source.classifications]);

  useEffect(() => {
    if (containerRef.current && containerWidth === 0) {
      setContainerWidth(containerRef.current.offsetWidth);
    }
  }, []);

  const grandmaClassifications = getGrandmaClassifications();
  const tags: ChipTag[] = (source.tags || []).map((tag: any) => ({
    id: tag.id,
    name: tag.name,
    objtagoption_id: tag.objtagoption_id,
    chipClass: "default",
    priority: 3,
  }));

  const allTags: ChipTag[] = [...grandmaClassifications, ...tags];
  const uniqueTags: ChipTag[] = [];
  const seenNames = new Set<string>();

  allTags.sort((a, b) => a.priority - b.priority);
  allTags.forEach((tag) => {
    if (!seenNames.has(tag.name.toLowerCase())) {
      seenNames.add(tag.name.toLowerCase());
      uniqueTags.push(tag);
    }
  });

  if (!displayTags || uniqueTags.length === 0) {
    return null;
  }

  const hasMoreTags = uniqueTags.length > visibleTagsCount;
  const visibleTags = uniqueTags.slice(0, visibleTagsCount);
  const hiddenTags = uniqueTags.slice(visibleTagsCount);

  const getChipClassName = (chipClass: string) => {
    switch (chipClass) {
      case "confirmed":
        return styles.confirmed;
      case "rejected":
        return styles.rejected;
      case "not_confirmed":
        return styles.not_confirmed;
      case "go":
        return styles.go;
      case "stop":
        return styles.stop;
      default:
        return styles.tagChip;
    }
  };

  const visibleTagsWithColors = visibleTags.map((tag) => {
    const tagOption = tagOptions.find(
      (option: any) => option.id === tag.objtagoption_id,
    );
    return {
      ...tag,
      color: tagOption?.color || "#dddfe2",
    };
  });

  const hiddenTagsWithColors = hiddenTags.map((tag) => {
    const tagOption = tagOptions.find(
      (option: any) => option.id === tag.objtagoption_id,
    );
    return {
      ...tag,
      color: tagOption?.color || "#dddfe2",
    };
  });

  return (
    <div className={styles.tagsContainer} ref={containerRef}>
      <span
        ref={measureRef}
        style={{ visibility: "hidden", position: "absolute" }}
      />

      {visibleTagsWithColors.map((tag) => (
        <Chip
          key={tag.id}
          label={tag.name}
          size="small"
          className={getChipClassName(tag.chipClass)}
          variant="filled"
          style={{
            backgroundColor: tag.color,
            color: getContrastColor(tag.color),
          }}
        />
      ))}

      {hasMoreTags && (
        <Tooltip
          title={
            <div>
              <strong>Additional tags:</strong>
              <br />
              {hiddenTagsWithColors.map((tag, index) => (
                <span key={tag.id}>
                  <Chip
                    label={tag.name}
                    size="small"
                    style={{
                      backgroundColor: tag.color,
                      color: getContrastColor(tag.color),
                      margin: "2px",
                    }}
                  />
                  {index < hiddenTagsWithColors.length - 1 ? " " : ""}
                </span>
              ))}
            </div>
          }
        >
          <Chip
            key="more-tags"
            label={`+${hiddenTags.length}`}
            size="small"
            className={styles.tagChip}
            color="default"
            variant="filled"
            style={{
              fontStyle: "italic",
              opacity: 0.7,
            }}
          />
        </Tooltip>
      )}
    </div>
  );
};

export default DynamicTagDisplay;
